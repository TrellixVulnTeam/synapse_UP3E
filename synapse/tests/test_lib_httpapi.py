import ssl
import json

import aiohttp
import aiohttp.client_exceptions as a_exc

import synapse.common as s_common
import synapse.lib.link as s_link
import synapse.lib.httpapi as s_httpapi
import synapse.lib.version as s_version

import synapse.tests.utils as s_tests

class HttpApiTest(s_tests.SynTest):

    async def test_reqauth(self):

        class ReqAuthHandler(s_httpapi.Handler):
            async def get(self):
                if not await self.allowed(('syn:test', )):
                    return
                return self.sendRestRetn({'data': 'everything is awesome!'})

        async with self.getTestCore() as core:
            core.addHttpApi('/api/tests/test_reqauth', ReqAuthHandler, {'cell': core})

            host, port = await core.addHttpsPort(0, host='127.0.0.1')
            url = f'https://localhost:{port}/api/tests/test_reqauth'
            root = await core.auth.getUserByName('root')
            await root.setPasswd('secret')

            user = await core.auth.addUser('user')
            await user.setPasswd('12345')

            async with self.getHttpSess(auth=('root', 'secret'), port=port) as sess:

                async with sess.get(url) as resp:
                    self.eq(resp.status, 200)
                    retn = await resp.json()
                    self.eq(retn.get('status'), 'ok')
                    self.eq(retn.get('result'), {'data': 'everything is awesome!'})

            async with self.getHttpSess(auth=('user', '12345'), port=port) as sess:
                async with sess.get(url) as resp:
                    self.eq(resp.status, 403)
                    retn = await resp.json()
                    self.eq(retn.get('status'), 'err')
                    self.eq(retn.get('code'), 'AuthDeny')

                await user.addRule((True, ('syn:test',)))

                async with sess.get(url) as resp:
                    self.eq(resp.status, 200)
                    retn = await resp.json()
                    self.eq(retn.get('status'), 'ok')
                    self.eq(retn.get('result'), {'data': 'everything is awesome!'})

            async with aiohttp.ClientSession() as sess:
                burl = f'https://newp:newp@localhost:{port}/api/tests/test_reqauth'
                async with sess.get(burl, ssl=False) as resp:
                    self.eq(resp.status, 401)
                    retn = await resp.json()
                    self.eq(retn.get('status'), 'err')

    async def test_http_user_archived(self):

        async with self.getTestCore() as core:

            host, port = await core.addHttpsPort(0, host='127.0.0.1')

            root = await core.auth.getUserByName('root')
            await root.setPasswd('secret')

            newb = await core.auth.addUser('newb')

            async with self.getHttpSess(auth=('root', 'secret'), port=port) as sess:

                async with sess.get(f'https://localhost:{port}/api/v1/auth/users') as resp:
                    item = await resp.json()
                    users = item.get('result')
                    self.isin('newb', [u.get('name') for u in users])

                info = {'archived': True}
                async with sess.post(f'https://localhost:{port}/api/v1/auth/user/{newb.iden}', json=info) as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))

                self.true(newb.isLocked())

                async with sess.get(f'https://localhost:{port}/api/v1/auth/users') as resp:
                    item = await resp.json()
                    users = item.get('result')
                    self.notin('newb', [u.get('name') for u in users])

                async with sess.get(f'https://localhost:{port}/api/v1/auth/users?archived=asdf') as resp:
                    item = await resp.json()
                    self.eq('err', item.get('status'))
                    self.eq('BadHttpParam', item.get('code'))

                async with sess.get(f'https://localhost:{port}/api/v1/auth/users?archived=99') as resp:
                    item = await resp.json()
                    self.eq('err', item.get('status'))
                    self.eq('BadHttpParam', item.get('code'))

                async with sess.get(f'https://localhost:{port}/api/v1/auth/users?archived=0') as resp:
                    item = await resp.json()
                    users = item.get('result')
                    self.notin('newb', [u.get('name') for u in users])

                async with sess.get(f'https://localhost:{port}/api/v1/auth/users?archived=1') as resp:
                    item = await resp.json()
                    users = item.get('result')
                    self.isin('newb', [u.get('name') for u in users])

                info = {'archived': False}
                async with sess.post(f'https://localhost:{port}/api/v1/auth/user/{newb.iden}', json=info) as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))

                async with sess.get(f'https://localhost:{port}/api/v1/auth/users') as resp:
                    item = await resp.json()
                    users = item.get('result')
                    self.isin('newb', [u.get('name') for u in users])

    async def test_http_delrole(self):

        async with self.getTestCore() as core:

            host, port = await core.addHttpsPort(0, host='127.0.0.1')

            root = await core.auth.getUserByName('root')
            await root.setPasswd('secret')

            newb = await core.auth.addUser('bob')
            await newb.setPasswd('secret')

            bobs = await core.auth.addRole('bobs')

            await newb.grant(bobs.iden)

            async with self.getHttpSess() as sess:

                info = {'name': 'bobs'}
                async with sess.post(f'https://localhost:{port}/api/v1/auth/delrole', json=info) as resp:
                    item = await resp.json()
                    self.eq('err', item.get('status'))
                    self.eq('NotAuthenticated', item.get('code'))

            async with self.getHttpSess(auth=('bob', 'secret'), port=port) as sess:

                info = {'name': 'bobs'}
                async with sess.post(f'https://localhost:{port}/api/v1/auth/delrole', json=info) as resp:
                    item = await resp.json()
                    self.eq('err', item.get('status'))
                    self.eq('AuthDeny', item.get('code'))

            async with self.getHttpSess(auth=('root', 'secret'), port=port) as sess:

                info = {}
                async with sess.post(f'https://localhost:{port}/api/v1/auth/delrole', json=info) as resp:
                    item = await resp.json()
                    self.eq('err', item.get('status'))
                    self.eq('MissingField', item.get('code'))

                async with sess.post(f'https://localhost:{port}/api/v1/auth/delrole', data=b'asdf') as resp:
                    item = await resp.json()
                    self.eq('err', item.get('status'))
                    self.eq('SchemaViolation', item.get('code'))

                info = {'name': 'newp'}
                async with sess.post(f'https://localhost:{port}/api/v1/auth/delrole', json=info) as resp:
                    item = await resp.json()
                    self.eq('err', item.get('status'))
                    self.eq('NoSuchRole', item.get('code'))

                self.len(2, newb.getRoles())
                info = {'name': 'bobs'}
                async with sess.post(f'https://localhost:{port}/api/v1/auth/delrole', json=info) as resp:
                    item = await resp.json()
                    self.eq('ok', item.get('status'))

            self.len(1, newb.getRoles())
            self.none(await core.auth.getRoleByName('bobs'))

    async def test_http_passwd(self):
        async with self.getTestCore() as core:

            host, port = await core.addHttpsPort(0, host='127.0.0.1')

            root = await core.auth.getUserByName('root')
            await root.setPasswd('secret')

            newb = await core.auth.addUser('newb')
            await newb.setPasswd('newb')

            async with self.getHttpSess(auth=('root', 'secret'), port=port) as sess:
                url = f'https://localhost:{port}/api/v1/auth/password/{newb.iden}'
                # Admin can change the newb password
                async with sess.post(url, json={'passwd': 'words'}) as resp:
                    item = await resp.json()
                    self.eq(item.get('status'), 'ok')

                # must have content
                async with sess.post(url) as resp:
                    item = await resp.json()
                    self.eq(item.get('status'), 'err')
                    self.isin('Invalid JSON content.', (item.get('mesg')))

                # password must be valid
                async with sess.post(url, json={'passwd': ''}) as resp:
                    item = await resp.json()
                    self.eq(item.get('status'), 'err')
                    self.eq(item.get('code'), 'BadArg')

                url = f'https://localhost:{port}/api/v1/auth/password/1234'
                # User iden must be valid
                async with sess.post(url, json={'passwd': 'words'}) as resp:
                    item = await resp.json()
                    self.isin('User does not exist', (item.get('mesg')))

            async with self.getHttpSess(auth=('newb', 'words'), port=port) as sess:
                # newb can change their own password
                url = f'https://localhost:{port}/api/v1/auth/password/{newb.iden}'
                async with sess.post(url, json={'passwd': 'newb'}) as resp:
                    item = await resp.json()
                    self.eq(item.get('status'), 'ok')

                # non-admin newb cannot change someone elses password
                url = f'https://localhost:{port}/api/v1/auth/password/{root.iden}'
                async with sess.post(url, json={'passwd': 'newb'}) as resp:
                    item = await resp.json()
                    self.eq(item.get('status'), 'ok')

    async def test_http_auth(self):
        '''
        Test the HTTP api for cell auth.
        '''
        async with self.getTestCore() as core:

            host, port = await core.addHttpsPort(0, host='127.0.0.1')
            root = await core.auth.getUserByName('root')
            await root.setPasswd('root')

            async with self.getHttpSess() as sess:

                info = {'name': 'visi', 'passwd': 'secret', 'admin': True}
                # Make the first user as root
                async with sess.post(f'https://root:root@localhost:{port}/api/v1/auth/adduser', json=info) as resp:
                    item = await resp.json()
                    self.nn(item.get('result').get('iden'))
                    visiiden = item['result']['iden']

                info = {'name': 'noob', 'passwd': 'nooblet', 'email': 'nobody@nowhere.com'}
                # The visi user is an admin, so reuse it
                async with sess.post(f'https://visi:secret@localhost:{port}/api/v1/auth/adduser', json=info) as resp:
                    item = await resp.json()
                    self.nn(item.get('result').get('iden'))
                    self.eq('nobody@nowhere.com', item['result']['email'])
                    noobiden = item['result']['iden']

                info = {'name': 'visi', 'passwd': 'secret', 'admin': True}
                async with sess.post(f'https://visi:secret@localhost:{port}/api/v1/auth/adduser', json=info) as resp:
                    item = await resp.json()
                    self.eq('err', item.get('status'))
                    self.eq('DupUser', item.get('code'))

                info = {'name': 'analysts'}
                async with sess.post(f'https://visi:secret@localhost:{port}/api/v1/auth/addrole', json=info) as resp:
                    item = await resp.json()
                    self.nn(item.get('result').get('iden'))
                    analystiden = item['result']['iden']

                info = {'name': 'analysts'}
                async with sess.post(f'https://visi:secret@localhost:{port}/api/v1/auth/addrole', json=info) as resp:
                    item = await resp.json()
                    self.eq('err', item.get('status'))
                    self.eq('DupRole', item.get('code'))

                async with sess.get(f'https://visi:secret@localhost:{port}/api/v1/auth/user/newp') as resp:
                    item = await resp.json()
                    self.eq('NoSuchUser', item.get('code'))

                async with sess.get(f'https://visi:secret@localhost:{port}/api/v1/auth/role/newp') as resp:
                    item = await resp.json()
                    self.eq('NoSuchRole', item.get('code'))

                async with sess.get(f'https://visi:secret@localhost:{port}/api/v1/auth/users') as resp:
                    item = await resp.json()
                    users = item.get('result')
                    self.isin('visi', [u.get('name') for u in users])

                async with sess.get(f'https://visi:secret@localhost:{port}/api/v1/auth/roles') as resp:
                    item = await resp.json()
                    roles = item.get('result')
                    self.isin('analysts', [r.get('name') for r in roles])

                info = {'user': 'blah', 'role': 'blah'}
                async with sess.post(f'https://visi:secret@localhost:{port}/api/v1/auth/grant', json=info) as resp:
                    item = await resp.json()
                    self.eq('NoSuchUser', item.get('code'))

                info = {'user': visiiden, 'role': 'blah'}
                async with sess.post(f'https://visi:secret@localhost:{port}/api/v1/auth/grant', json=info) as resp:
                    item = await resp.json()
                    self.eq('NoSuchRole', item.get('code'))

                info = {'user': 'blah', 'role': 'blah'}
                async with sess.post(f'https://visi:secret@localhost:{port}/api/v1/auth/revoke', json=info) as resp:
                    item = await resp.json()
                    self.eq('NoSuchUser', item.get('code'))

                info = {'user': visiiden, 'role': 'blah'}
                async with sess.post(f'https://visi:secret@localhost:{port}/api/v1/auth/revoke', json=info) as resp:
                    item = await resp.json()
                    self.eq('NoSuchRole', item.get('code'))

                info = {'user': visiiden, 'role': analystiden}
                async with sess.post(f'https://visi:secret@localhost:{port}/api/v1/auth/grant', json=info) as resp:
                    item = await resp.json()
                    self.eq('ok', item.get('status'))
                    roles = item['result']['roles']
                    self.len(2, roles)
                    self.isin(analystiden, roles)

                info = {'user': visiiden, 'role': analystiden}
                async with sess.post(f'https://visi:secret@localhost:{port}/api/v1/auth/revoke', json=info) as resp:
                    item = await resp.json()
                    self.eq('ok', item.get('status'))
                    roles = item['result']['roles']
                    self.len(1, roles)

            # lets try out session based login

            async with self.getHttpSess() as sess:

                info = {'user': 'hehe'}
                async with sess.post(f'https://localhost:{port}/api/v1/login', json=info) as resp:
                    item = await resp.json()
                    self.eq('AuthDeny', item.get('code'))

            async with self.getHttpSess() as sess:

                info = {'user': 'visi', 'passwd': 'borked'}
                async with sess.post(f'https://localhost:{port}/api/v1/login', json=info) as resp:
                    item = await resp.json()
                    self.eq('AuthDeny', item.get('code'))

            async with self.getHttpSess() as sess:

                async with sess.post(f'https://localhost:{port}/api/v1/auth/adduser', json=info) as resp:
                    item = await resp.json()
                    self.eq('NotAuthenticated', item.get('code'))

                visiauth = aiohttp.BasicAuth('visi', 'secret')
                newpauth = aiohttp.BasicAuth('visi', 'newp')

                async with sess.get(f'https://localhost:{port}/api/v1/auth/users', auth=visiauth) as resp:
                    item = await resp.json()
                    self.eq('ok', item.get('status'))

                async with sess.get(f'https://localhost:{port}/api/v1/auth/users', auth=newpauth) as resp:
                    item = await resp.json()
                    self.eq('NotAuthenticated', item.get('code'))

                headers = {'Authorization': 'yermom'}
                async with sess.get(f'https://localhost:{port}/api/v1/auth/users', headers=headers) as resp:
                    item = await resp.json()
                    self.eq('NotAuthenticated', item.get('code'))

                headers = {'Authorization': 'Basic zzzz'}
                async with sess.get(f'https://localhost:{port}/api/v1/auth/users', headers=headers) as resp:
                    item = await resp.json()
                    self.eq('NotAuthenticated', item.get('code'))

            # work some authenticated as admin code paths
            async with self.getHttpSess() as sess:

                async with sess.post(f'https://localhost:{port}/api/v1/login', json={'user': 'visi', 'passwd': 'secret'}) as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))
                    self.eq('visi', retn['result']['name'])

                # check same-host cross-origin behavior
                origin = 'https://localhost:1/web/site'
                headers = {'origin': origin}
                async with sess.get(f'https://localhost:{port}/api/v1/auth/users', headers=headers) as resp:
                    retn = await resp.json()
                    self.eq(origin, resp.headers.get('Access-Control-Allow-Origin'))
                    self.eq('ok', retn.get('status'))

                # check same-host cross-origin options
                origin = 'https://localhost:1/web/site'
                headers = {'origin': origin}
                async with sess.options(f'https://localhost:{port}/api/v1/auth/users', headers=headers) as resp:
                    self.eq(origin, resp.headers.get('Access-Control-Allow-Origin'))
                    self.eq(204, resp.status)

                # use the authenticated session to do stuff...
                async with sess.get(f'https://localhost:{port}/api/v1/auth/users') as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))

                info = {'rules': ()}
                async with sess.post(f'https://localhost:{port}/api/v1/auth/user/{visiiden}', json=info) as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))

                info = {'locked': True, 'name': 'derpderp', 'email': 'noob@derp.com'}
                async with sess.post(f'https://localhost:{port}/api/v1/auth/user/{noobiden}', json=info) as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))
                    self.eq(True, retn['result']['locked'])
                    self.eq('derpderp', retn['result']['name'])
                    self.eq('noob@derp.com', retn['result']['email'])
                    self.eq(noobiden, retn['result']['iden'])

                async with self.getHttpSess() as noobsess:
                    info = {'user': 'noob', 'passwd': 'nooblet'}
                    async with sess.post(f'https://localhost:{port}/api/v1/login', json=info) as resp:
                        item = await resp.json()
                        self.eq('AuthDeny', item.get('code'))

                info = {'locked': False}
                async with sess.post(f'https://localhost:{port}/api/v1/auth/user/{noobiden}', json=info) as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))
                    self.false(retn['result']['locked'])
                    self.eq('derpderp', retn['result']['name'])
                    self.eq(noobiden, retn['result']['iden'])

                info = {'rules': ()}
                async with sess.post(f'https://localhost:{port}/api/v1/auth/role/{analystiden}', json=info) as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))

                async with sess.post(f'https://localhost:{port}/api/v1/auth/adduser', json={}) as resp:
                    item = await resp.json()
                    self.eq('MissingField', item.get('code'))

                async with sess.post(f'https://localhost:{port}/api/v1/auth/addrole', json={}) as resp:
                    item = await resp.json()
                    self.eq('MissingField', item.get('code'))

                async with sess.post(f'https://localhost:{port}/api/v1/auth/adduser', data=b'asdf') as resp:
                    item = await resp.json()
                    self.eq('SchemaViolation', item.get('code'))

                async with sess.post(f'https://localhost:{port}/api/v1/auth/addrole', data=b'asdf') as resp:
                    item = await resp.json()
                    self.eq('SchemaViolation', item.get('code'))

                async with sess.post(f'https://localhost:{port}/api/v1/auth/grant', data=b'asdf') as resp:
                    item = await resp.json()
                    self.eq('SchemaViolation', item.get('code'))

                async with sess.post(f'https://localhost:{port}/api/v1/auth/revoke', data=b'asdf') as resp:
                    item = await resp.json()
                    self.eq('SchemaViolation', item.get('code'))

                async with sess.post(f'https://localhost:{port}/api/v1/auth/user/{visiiden}', data=b'asdf') as resp:
                    item = await resp.json()
                    self.eq('SchemaViolation', item.get('code'))

                async with sess.post(f'https://localhost:{port}/api/v1/auth/role/{analystiden}', data=b'asdf') as resp:
                    item = await resp.json()
                    self.eq('SchemaViolation', item.get('code'))

                async with sess.get(f'https://localhost:{port}/api/v1/storm/nodes', data=b'asdf') as resp:
                    item = await resp.json()
                    self.eq('SchemaViolation', item.get('code'))

                rules = [(True, ('node', 'add',))]
                info = {'name': 'derpuser', 'passwd': 'derpuser', 'rules': rules}
                async with sess.post(f'https://localhost:{port}/api/v1/auth/adduser', json=info) as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))
                    user = retn.get('result')
                    derpiden = user.get('iden')
                    self.eq('derpuser', user.get('name'))
                    self.len(1, user.get('rules'))
                    self.false(user.get('admin'))

                info = {'admin': True}
                async with sess.post(f'https://localhost:{port}/api/v1/auth/user/{derpiden}', json=info) as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))
                    user = retn.get('result')
                    self.true(user.get('admin'))

                info = {'admin': False}
                async with sess.post(f'https://localhost:{port}/api/v1/auth/user/{derpiden}', json=info) as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))
                    user = retn.get('result')
                    self.false(user.get('admin'))

            # test some auth but not admin paths
            async with self.getHttpSess() as sess:

                async with sess.post(f'https://localhost:{port}/api/v1/login', data=b'asdf') as resp:
                    retn = await resp.json()
                    self.eq('SchemaViolation', retn.get('code'))

                async with sess.post(f'https://localhost:{port}/api/v1/login',
                                     json={'user': 'derpuser', 'passwd': 'derpuser'}) as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))
                    self.eq('derpuser', retn['result']['name'])

                info = {'admin': True}
                async with sess.post(f'https://localhost:{port}/api/v1/auth/user/{derpiden}', json=info) as resp:
                    retn = await resp.json()
                    self.eq('AuthDeny', retn.get('code'))

                info = {'rules': ()}
                async with sess.post(f'https://localhost:{port}/api/v1/auth/role/{analystiden}', json=info) as resp:
                    retn = await resp.json()
                    self.eq('AuthDeny', retn.get('code'))

                async with sess.post(f'https://localhost:{port}/api/v1/auth/grant', json={}) as resp:
                    retn = await resp.json()
                    self.eq('AuthDeny', retn.get('code'))

                async with sess.post(f'https://localhost:{port}/api/v1/auth/revoke', json={}) as resp:
                    retn = await resp.json()
                    self.eq('AuthDeny', retn.get('code'))

                async with sess.post(f'https://localhost:{port}/api/v1/auth/adduser', json={}) as resp:
                    retn = await resp.json()
                    self.eq('AuthDeny', retn.get('code'))

                async with sess.post(f'https://localhost:{port}/api/v1/auth/addrole', json={}) as resp:
                    retn = await resp.json()
                    self.eq('AuthDeny', retn.get('code'))

    async def test_http_impersonate(self):

        async with self.getTestCore() as core:

            host, port = await core.addHttpsPort(0, host='127.0.0.1')

            visi = await core.auth.addUser('visi')

            await visi.setPasswd('secret')
            await visi.addRule((True, ('impersonate',)))

            opts = {'user': core.auth.rootuser.iden}

            async with self.getHttpSess() as sess:

                async with sess.post(f'https://localhost:{port}/api/v1/login', json={'user': 'visi', 'passwd': 'secret'}) as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))

                data = {'query': '[ inet:ipv4=1.2.3.4 ]', 'opts': opts}

                podes = []
                async with sess.get(f'https://localhost:{port}/api/v1/storm/nodes', json=data) as resp:

                    async for byts, x in resp.content.iter_chunks():

                        if not byts:
                            break

                        podes.append(json.loads(byts))

                self.eq(podes[0][0], ('inet:ipv4', 0x01020304))

                msgs = []
                data = {'query': '[ inet:ipv4=5.5.5.5 ]', 'opts': opts}

                async with sess.get(f'https://localhost:{port}/api/v1/storm', json=data) as resp:

                    async for byts, x in resp.content.iter_chunks():

                        if not byts:
                            break

                        msgs.append(json.loads(byts))
                podes = [m[1] for m in msgs if m[0] == 'node']
                self.eq(podes[0][0], ('inet:ipv4', 0x05050505))

    async def test_http_coreinfo(self):
        async with self.getTestCore() as core:

            visi = await core.auth.addUser('visi')

            await visi.setAdmin(True)
            await visi.setPasswd('secret')

            host, port = await core.addHttpsPort(0, host='127.0.0.1')

            async with self.getHttpSess() as sess:

                async with sess.post(f'https://localhost:{port}/api/v1/login',
                                     json={'user': 'visi', 'passwd': 'secret'}) as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))
                    self.eq('visi', retn['result']['name'])

                async with sess.get(f'https://localhost:{port}/api/v1/core/info') as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))
                    coreinfo = retn.get('result')

                self.eq(coreinfo.get('version'), s_version.version)

                self.nn(coreinfo.get('modeldict'))

                docs = coreinfo.get('stormdocs')
                self.isin('types', docs)
                self.isin('libraries', docs)

            # Auth failures
            conn = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(connector=conn) as sess:
                async with sess.get(f'https://visi:newp@localhost:{port}/api/v1/core/info') as resp:
                    retn = await resp.json()
                    self.eq('err', retn.get('status'))

    async def test_http_model(self):

        async with self.getTestCore() as core:

            visi = await core.auth.addUser('visi')

            await visi.setAdmin(True)
            await visi.setPasswd('secret')

            host, port = await core.addHttpsPort(0, host='127.0.0.1')

            async with self.getHttpSess() as sess:

                self.len(0, core.sessions)  # zero sessions..

                async with sess.post(f'https://localhost:{port}/api/v1/login',
                                     json={'user': 'visi', 'passwd': 'secret'}) as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))
                    self.eq('visi', retn['result']['name'])

                self.len(1, core.sessions)  # We have one session after login

                # Get a copy of the data model
                async with sess.get(f'https://localhost:{port}/api/v1/model') as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))
                    self.isin('types', retn['result'])
                    self.isin('forms', retn['result'])

                self.len(1, core.sessions)  # We still have one session since the cookie was reused

                # Norm via GET
                body = {'prop': 'inet:ipv4', 'value': '1.2.3.4'}
                async with sess.get(f'https://localhost:{port}/api/v1/model/norm', json=body) as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))
                    self.eq(0x01020304, retn['result']['norm'])
                    self.eq('unicast', retn['result']['info']['subs']['type'])

                body = {'prop': 'fake:prop', 'value': '1.2.3.4'}
                async with sess.get(f'https://localhost:{port}/api/v1/model/norm', json=body) as resp:
                    retn = await resp.json()
                    self.eq('NoSuchProp', retn.get('code'))

                body = {'value': '1.2.3.4'}
                async with sess.get(f'https://localhost:{port}/api/v1/model/norm', json=body) as resp:
                    retn = await resp.json()
                    self.eq('MissingField', retn.get('code'))

                # Norm via POST
                body = {'prop': 'inet:ipv4', 'value': '1.2.3.4'}
                async with sess.post(f'https://localhost:{port}/api/v1/model/norm', json=body) as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))
                    self.eq(0x01020304, retn['result']['norm'])
                    self.eq('unicast', retn['result']['info']['subs']['type'])

            # Auth failures
            conn = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(connector=conn) as sess:
                async with sess.get(f'https://visi:newp@localhost:{port}/api/v1/model') as resp:
                    retn = await resp.json()
                    self.eq('err', retn.get('status'))

                body = {'prop': 'inet:ipv4', 'value': '1.2.3.4'}
                async with sess.get(f'https://visi:newp@localhost:{port}/api/v1/model/norm', json=body) as resp:
                    retn = await resp.json()
                    self.eq('err', retn.get('status'))

    async def test_http_watch(self):

        async with self.getTestCore() as core:

            visi = await core.auth.addUser('visi')

            await visi.setPasswd('secret')

            host, port = await core.addHttpsPort(0, host='127.0.0.1')

            # with no session user...
            async with self.getHttpSess() as sess:

                async with sess.ws_connect(f'wss://localhost:{port}/api/v1/watch') as sock:
                    await sock.send_json({'tags': ['test.visi']})
                    mesg = await sock.receive_json()
                    self.eq('errx', mesg['type'])
                    self.eq('AuthDeny', mesg['data']['code'])

                async with sess.post(f'https://localhost:{port}/api/v1/login', json={'user': 'visi', 'passwd': 'secret'}) as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))
                    self.eq('visi', retn['result']['name'])

                async with sess.ws_connect(f'wss://localhost:{port}/api/v1/watch') as sock:
                    await sock.send_json({'tags': ['test.visi']})
                    mesg = await sock.receive_json()
                    self.eq('errx', mesg['type'])
                    self.eq('AuthDeny', mesg['data']['code'])

                await visi.addRule((True, ('watch',)))

                async with sess.ws_connect(f'wss://localhost:{port}/api/v1/watch') as sock:

                    await sock.send_json({'tags': ['test.visi']})
                    mesg = await sock.receive_json()

                    self.eq('init', mesg['type'])

                    await core.nodes('[ test:str=woot +#test.visi ]')

                    mesg = await sock.receive_json()

                    self.eq('tag:add', mesg['type'])
                    self.eq('test.visi', mesg['data']['tag'])

    async def test_http_beholder(self):
        async with self.getTestCore() as core:

            visi = await core.auth.addUser('visi')

            await visi.setPasswd('secret')

            host, port = await core.addHttpsPort(0, host='127.0.0.1')

            async with self.getHttpSess() as sess:

                async with sess.ws_connect(f'wss://localhost:{port}/api/v1/behold') as sock:
                    await sock.send_json({'type': 'call:init'})
                    mesg = await sock.receive_json()
                    self.eq('errx', mesg['type'])
                    self.eq('AuthDeny', mesg['data']['code'])

                async with sess.post(f'https://localhost:{port}/api/v1/login', json={'user': 'visi', 'passwd': 'secret'}) as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))
                    self.eq('visi', retn['result']['name'])

                async with sess.ws_connect(f'wss://localhost:{port}/api/v1/behold') as sock:
                    await sock.send_json({'type': 'call:init'})
                    mesg = await sock.receive_json()
                    self.eq('errx', mesg['type'])
                    self.eq('AuthDeny', mesg['data']['code'])

                await visi.setAdmin(True)

                async with sess.ws_connect(f'wss://localhost:{port}/api/v1/behold') as sock:
                    await sock.send_json({'type': 'bleep blorp'})
                    mesg = await sock.receive_json()
                    self.eq('errx', mesg['type'])
                    self.eq('BadMesgFormat', mesg['data']['code'])

                ssvc = {'iden': s_common.guid(), 'name': 'dups', 'url': 'tcp://127.0.0.1:1/'}
                spkg = {
                    'name': 'testy',
                    'version': (0, 0, 1),
                    'synapse_minversion': (2, 50, 0),
                    'modules': (
                        {'name': 'testy.ingest', 'storm': 'function punch(x, y) { return (($x + $y)) }'},
                    ),
                    'commands': (
                        {
                            'name': 'testy.dostuff',
                            'storm': '$ingest = $lib.import("test.ingest") $punch.punch(40, 20)'
                        },
                    ),
                    'perms': (
                        {
                            'perm': ('test', 'testy', 'permission'),
                            'gate': 'cortex',
                            'desc': 'a test gate',
                        },
                    ),
                }

                async with sess.ws_connect(f'wss://localhost:{port}/api/v1/behold') as sock:
                    root = await core.auth.getUserByName('root')
                    await sock.send_json({'type': 'call:init'})
                    mesg = await sock.receive_json()
                    self.eq(mesg['type'], 'init')

                    base = 0
                    layr, view = await core.callStorm('''
                        $view = $lib.view.get().fork()
                        return(($view.layers.0.iden, $view.iden))
                    ''')
                    mesg = await sock.receive_json()
                    self.eq(mesg['type'], 'iter')
                    data = mesg['data']
                    self.len(1, data['gates'])
                    self.eq(data['event'], 'layer:add')
                    self.gt(data['offset'], base)
                    base = data['offset']

                    info = data['info']
                    self.eq(info['creator'], root.iden)
                    self.eq(info['iden'], layr)

                    gate = data['gates'][0]
                    self.eq(gate['iden'], layr)
                    self.eq(gate['type'], 'layer')
                    self.len(1, gate['users'])

                    user = gate['users'][0]
                    self.eq(user['iden'], root.iden)
                    self.true(user['admin'])

                    mesg = await sock.receive_json()
                    self.eq(mesg['type'], 'iter')
                    data = mesg['data']
                    info = data['info']
                    self.eq(data['event'], 'view:add')
                    self.gt(data['offset'], base)
                    base = data['offset']

                    self.eq(info['creator'], root.iden)
                    self.eq(info['iden'], view)

                    cdef = await core.callStorm('return($lib.cron.add(query="{graph:node=*}", hourly=30).pack())')
                    layr = await core.callStorm('return($lib.layer.add().iden)')

                    opts = {'vars': {'view': view, 'cron': cdef['iden'], 'layr': layr}}
                    await core.callStorm('$lib.view.get($view).set(name, "a really okay view")', opts=opts)
                    await core.callStorm('$lib.layer.get($layr).set(name, "some kinda layer")', opts=opts)
                    await core.callStorm('cron.move $cron $view', opts=opts)
                    await core.callStorm('cron.mod $cron {[test:guid=*]}', opts=opts)
                    await core.callStorm('cron.disable $cron', opts=opts)
                    await core.callStorm('cron.enable $cron', opts=opts)
                    await core.callStorm('$c = $lib.cron.get($cron) $c.set("name", "neato cron")', opts=opts)
                    await core.callStorm('$c = $lib.cron.get($cron) $c.set("doc", "some docs")', opts=opts)
                    await core.callStorm('cron.del $cron', opts=opts)

                    await core.addStormPkg(spkg)
                    await core.addStormSvc(ssvc)

                    await core.delStormSvc(ssvc['iden'])
                    await core.delStormPkg(spkg['name'])

                    await core.callStorm('view.del $view', opts=opts)
                    await core.callStorm('$lib.layer.del($layr)', opts=opts)

                    events = [
                        'cron:add',
                        'layer:add',
                        'view:set',
                        'layer:set',
                        'cron:move',
                        'cron:edit:query',
                        'cron:disable',
                        'cron:enable',
                        'cron:edit:name',
                        'cron:edit:doc',
                        'cron:del',
                        'pkg:add',
                        'svc:add',
                        'svc:del',
                        'pkg:del',
                        'view:del',
                        'layer:del',
                    ]

                    mesgs = []
                    for event in events:
                        m = await sock.receive_json()
                        self.eq(m['type'], 'iter')
                        data = m.get('data')
                        self.nn(data)
                        self.nn(data['info'])
                        self.ge(len(data['info']), 1)
                        self.eq(event, data['event'])

                        if not event.startswith('svc'):
                            self.nn(data['gates'])
                            self.ge(len(data['gates']), 1)

                        if event.startswith('pkg'):
                            self.len(1, data['perms'])

                        # offset always goes up
                        self.gt(data['offset'], base)
                        base = data['offset']
                        mesgs.append(data)

    async def test_http_storm(self):

        async with self.getTestCore() as core:

            visi = await core.auth.addUser('visi')

            await visi.setPasswd('secret')

            host, port = await core.addHttpsPort(0, host='127.0.0.1')

            async with self.getHttpSess(port=port) as sess:
                resp = await sess.post(f'https://localhost:{port}/api/v1/storm')
                self.eq(401, resp.status)

            async with self.getHttpSess() as sess:

                async with sess.post(f'https://localhost:{port}/api/v1/login', json={'user': 'visi', 'passwd': 'secret'}) as resp:
                    retn = await resp.json()
                    self.eq('ok', retn.get('status'))
                    self.eq('visi', retn['result']['name'])

                body = {'query': 'inet:ipv4', 'opts': {'user': core.auth.rootuser.iden}}
                async with sess.get(f'https://localhost:{port}/api/v1/storm', json=body) as resp:
                    self.eq(resp.status, 403)

                body = {'query': 'inet:ipv4', 'opts': {'user': core.auth.rootuser.iden}}
                async with sess.get(f'https://localhost:{port}/api/v1/storm/nodes', json=body) as resp:
                    self.eq(resp.status, 403)

                await visi.setAdmin(True)

                async with sess.get(f'https://localhost:{port}/api/v1/storm', data=b'asdf') as resp:
                    item = await resp.json()
                    self.eq('SchemaViolation', item.get('code'))

                node = None
                body = {'query': '[ inet:ipv4=1.2.3.4 ]'}

                async with sess.get(f'https://localhost:{port}/api/v1/storm', json=body) as resp:

                    async for byts, x in resp.content.iter_chunks():

                        if not byts:
                            break

                        mesg = json.loads(byts)

                        if mesg[0] == 'node':
                            node = mesg[1]

                    self.nn(node)
                    self.eq(0x01020304, node[0][1])

                async with sess.post(f'https://localhost:{port}/api/v1/storm', json=body) as resp:

                    async for byts, x in resp.content.iter_chunks():

                        if not byts:
                            break

                        mesg = json.loads(byts)

                        if mesg[0] == 'node':
                            node = mesg[1]

                    self.eq(0x01020304, node[0][1])

                node = None
                body = {'query': '[ inet:ipv4=1.2.3.4 ]'}

                async with sess.get(f'https://localhost:{port}/api/v1/storm/nodes', json=body) as resp:

                    async for byts, x in resp.content.iter_chunks():

                        if not byts:
                            break

                        node = json.loads(byts)

                    self.eq(0x01020304, node[0][1])

                async with sess.post(f'https://localhost:{port}/api/v1/storm/nodes', json=body) as resp:

                    async for byts, x in resp.content.iter_chunks():

                        if not byts:
                            break

                        node = json.loads(byts)

                    self.eq(0x01020304, node[0][1])

                body['stream'] = 'jsonlines'

                async with sess.get(f'https://localhost:{port}/api/v1/storm/nodes', json=body) as resp:
                    bufr = b''
                    async for byts, x in resp.content.iter_chunks():

                        if not byts:
                            break

                        bufr += byts
                        for jstr in bufr.split(b'\n'):
                            if not jstr:
                                bufr = b''
                                break

                            try:
                                node = json.loads(byts)
                            except json.JSONDecodeError:
                                bufr = jstr
                                break

                    self.eq(0x01020304, node[0][1])

                async with sess.post(f'https://localhost:{port}/api/v1/storm', json=body) as resp:

                    bufr = b''
                    async for byts, x in resp.content.iter_chunks():

                        if not byts:
                            break

                        bufr += byts
                        for jstr in bufr.split(b'\n'):
                            if not jstr:
                                bufr = b''
                                break

                            try:
                                mesg = json.loads(byts)
                            except json.JSONDecodeError:
                                bufr = jstr
                                break

                            if mesg[0] == 'node':
                                node = mesg[1]

                    self.eq(0x01020304, node[0][1])

                # Task cancellation during long running storm queries works as intended
                body = {'query': '.created | sleep 10'}
                task = None
                async with sess.get(f'https://localhost:{port}/api/v1/storm', json=body) as resp:

                    async for byts, x in resp.content.iter_chunks():

                        if not byts:
                            break

                        mesg = json.loads(byts)
                        if mesg[0] == 'node':
                            task = core.boss.tasks.get(list(core.boss.tasks.keys())[0])
                            break

                self.nn(task)
                self.true(await task.waitfini(6))
                self.len(0, core.boss.tasks)

                task = None
                async with sess.get(f'https://localhost:{port}/api/v1/storm/nodes', json=body) as resp:

                    async for byts, x in resp.content.iter_chunks():

                        if not byts:
                            break

                        mesg = json.loads(byts)
                        self.len(2, mesg)  # Is if roughly shaped like a node?
                        task = core.boss.tasks.get(list(core.boss.tasks.keys())[0])
                        break

                self.nn(task)
                self.true(await task.waitfini(6))
                self.len(0, core.boss.tasks)

                # check reqvalidstorm with various queries
                tvs = (
                    ('test:str=test', {}, 'ok'),
                    ('1.2.3.4 | spin', {'mode': 'lookup'}, 'ok'),
                    ('1.2.3.4 | spin', {'mode': 'autoadd'}, 'ok'),
                    ('1.2.3.4', {}, 'err'),
                    ('| 1.2.3.4 ', {'mode': 'lookup'}, 'err'),
                    ('| 1.2.3.4', {'mode': 'autoadd'}, 'err'),
                )
                url = f'https://localhost:{port}/api/v1/reqvalidstorm'
                for (query, opts, rcode) in tvs:
                    body = {'query': query, 'opts': opts}
                    async with sess.post(url, json=body) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            self.eq(data.get('status'), rcode)
                # Sad path
                async with aiohttp.client.ClientSession() as bad_sess:
                    async with bad_sess.post(url, ssl=False) as resp:
                        data = await resp.json()
                        self.eq(data.get('status'), 'err')
                        self.eq(data.get('code'), 'NotAuthenticated')

    async def test_tls_ciphers(self):

        async with self.getTestCore() as core:

            host, port = await core.addHttpsPort(0, host='127.0.0.1')

            with self.raises(ssl.SSLError):
                sslctx = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1)
                link = await s_link.connect('127.0.0.1', port=port, ssl=sslctx)

            with self.raises(ssl.SSLError):
                sslctx = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_1)
                link = await s_link.connect('127.0.0.1', port=port, ssl=sslctx)

            with self.raises(ssl.SSLError):
                sslctx = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_2)
                sslctx.set_ciphers('ADH-AES256-SHA')
                link = await s_link.connect('127.0.0.1', port=port, ssl=sslctx)

            with self.raises(ssl.SSLError):
                sslctx = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_2)
                sslctx.set_ciphers('DHE-RSA-AES256-SHA256')
                link = await s_link.connect('127.0.0.1', port=port, ssl=sslctx)

    async def test_healthcheck(self):
        conf = {
            'https:headers': {
                'X-Hehe-Haha': 'wootwoot!',
            }
        }
        async with self.getTestCore(conf=conf) as core:
            # Run http instead of https for this test
            host, port = await core.addHttpsPort(0, host='127.0.0.1')

            root = await core.auth.getUserByName('root')

            async with self.getHttpSess(auth=None, port=port) as sess:

                url = f'https://localhost:{port}/robots.txt'
                async with sess.get(url) as resp:
                    self.eq('User-agent: *\nDisallow: /\n', await resp.text())

                url = f'https://localhost:{port}/api/v1/active'
                async with sess.get(url) as resp:
                    self.none(resp.headers.get('server'))
                    self.eq('wootwoot!', resp.headers.get('x-hehe-haha'))
                    result = await resp.json()
                    self.eq(result.get('status'), 'ok')
                    self.true(result['result']['active'])
                    self.eq('1; mode=block', resp.headers.get('x-xss-protection'))
                    self.eq('nosniff', resp.headers.get('x-content-type-options'))

            await root.setPasswd('secret')

            url = f'https://localhost:{port}/api/v1/healthcheck'
            async with self.getHttpSess(auth=('root', 'secret'), port=port) as sess:
                async with sess.get(url) as resp:
                    result = await resp.json()
                    self.eq(result.get('status'), 'ok')
                    snfo = result.get('result')
                    self.isinstance(snfo, dict)
                    self.eq(snfo.get('status'), 'nominal')

            user = await core.auth.addUser('user')
            await user.setPasswd('beep')
            async with self.getHttpSess(auth=('user', 'beep'), port=port) as sess:
                async with sess.get(url) as resp:
                    result = await resp.json()
                    self.eq(result.get('status'), 'err')
                await user.addRule((True, ('health',)))
                async with sess.get(url) as resp:
                    result = await resp.json()
                    self.eq(result.get('status'), 'ok')

    async def test_streamhandler(self):

        class SadHandler(s_httpapi.StreamHandler):
            '''
            data_received must be implemented
            '''
            async def post(self):
                self.sendRestRetn('foo')
                return

        async with self.getTestCore() as core:
            core.addHttpApi('/api/v1/sad', SadHandler, {'cell': core})

            host, port = await core.addHttpsPort(0, host='127.0.0.1')

            root = await core.auth.getUserByName('root')
            await root.setPasswd('secret')

            url = f'https://localhost:{port}/api/v1/sad'
            async with self.getHttpSess(auth=('root', 'secret'), port=port) as sess:
                with self.raises(a_exc.ServerDisconnectedError):
                    async with sess.post(url, data=b'foo') as resp:
                        pass

    async def test_http_storm_vars(self):

        async with self.getTestCore() as core:

            host, port = await core.addHttpsPort(0, host='127.0.0.1')

            root = core.auth.rootuser
            visi = await core.auth.addUser('visi')

            await visi.setPasswd('secret')
            await root.setPasswd('secret')

            async with self.getHttpSess(auth=('root', 'secret'), port=port) as sess:

                resp = await sess.post(f'https://localhost:{port}/api/v1/storm/vars/set')
                self.eq('SchemaViolation', (await resp.json())['code'])

                resp = await sess.get(f'https://localhost:{port}/api/v1/storm/vars/get')
                self.eq('SchemaViolation', (await resp.json())['code'])

                resp = await sess.post(f'https://localhost:{port}/api/v1/storm/vars/pop')
                self.eq('SchemaViolation', (await resp.json())['code'])

                body = {'name': 'hehe'}
                resp = await sess.post(f'https://localhost:{port}/api/v1/storm/vars/set', json=body)
                self.eq('BadArg', (await resp.json())['code'])

                body = {'name': 'hehe', 'value': 'haha'}
                resp = await sess.post(f'https://localhost:{port}/api/v1/storm/vars/set', json=body)
                self.eq({'status': 'ok', 'result': True}, await resp.json())

                body = {'name': 'hehe', 'default': 'lolz'}
                resp = await sess.get(f'https://localhost:{port}/api/v1/storm/vars/get', json=body)
                self.eq({'status': 'ok', 'result': 'haha'}, await resp.json())

                body = {'name': 'hehe', 'default': 'lolz'}
                resp = await sess.post(f'https://localhost:{port}/api/v1/storm/vars/pop', json=body)
                self.eq({'status': 'ok', 'result': 'haha'}, await resp.json())

            async with self.getHttpSess(auth=('visi', 'secret'), port=port) as sess:

                body = {'name': 'hehe', 'value': 'haha'}
                resp = await sess.post(f'https://localhost:{port}/api/v1/storm/vars/set', json=body)
                self.eq('AuthDeny', (await resp.json())['code'])

                body = {'name': 'hehe', 'default': 'lolz'}
                resp = await sess.get(f'https://localhost:{port}/api/v1/storm/vars/get', json=body)
                self.eq('AuthDeny', (await resp.json())['code'])

                body = {'name': 'hehe', 'default': 'lolz'}
                resp = await sess.post(f'https://localhost:{port}/api/v1/storm/vars/pop', json=body)
                self.eq('AuthDeny', (await resp.json())['code'])

    async def test_http_feed(self):

        async with self.getTestCore() as core:

            host, port = await core.addHttpsPort(0, host='127.0.0.1')

            root = core.auth.rootuser
            visi = await core.auth.addUser('visi')

            await visi.setPasswd('secret')
            await root.setPasswd('secret')

            async with self.getHttpSess(port=port) as sess:
                body = {'items': [(('inet:ipv4', 0x05050505), {})]}
                resp = await sess.post(f'https://localhost:{port}/api/v1/feed', json=body)
                self.eq('NotAuthenticated', (await resp.json())['code'])

            async with self.getHttpSess(auth=('root', 'secret'), port=port) as sess:
                resp = await sess.post(f'https://localhost:{port}/api/v1/feed')
                self.eq('SchemaViolation', (await resp.json())['code'])

                body = {'view': 'asdf'}
                resp = await sess.post(f'https://localhost:{port}/api/v1/feed', json=body)
                self.eq('NoSuchView', (await resp.json())['code'])

                body = {'name': 'asdf'}
                resp = await sess.post(f'https://localhost:{port}/api/v1/feed', json=body)
                self.eq('NoSuchFunc', (await resp.json())['code'])

                body = {'items': [(('inet:ipv4', 0x05050505), {'tags': {'hehe': (None, None)}})]}
                resp = await sess.post(f'https://localhost:{port}/api/v1/feed', json=body)
                self.eq('ok', (await resp.json())['status'])
                self.len(1, await core.nodes('inet:ipv4=5.5.5.5 +#hehe'))

            async with self.getHttpSess(auth=('visi', 'secret'), port=port) as sess:
                body = {'items': [(('inet:ipv4', 0x01020304), {})]}
                resp = await sess.post(f'https://localhost:{port}/api/v1/feed', json=body)
                self.eq('AuthDeny', (await resp.json())['code'])
                self.len(0, await core.nodes('inet:ipv4=1.2.3.4'))
