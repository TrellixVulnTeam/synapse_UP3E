import os
import asyncio

from unittest import mock

import synapse.exc as s_exc
import synapse.axon as s_axon
import synapse.common as s_common
import synapse.telepath as s_telepath

import synapse.lib.aha as s_aha
import synapse.lib.output as s_output

import synapse.tools.backup as s_tools_backup

import synapse.tools.aha.enroll as s_tools_enroll
import synapse.tools.aha.provision.user as s_tools_provision_user
import synapse.tools.aha.provision.service as s_tools_provision_service

import synapse.tests.utils as s_test

realaddsvc = s_aha.AhaCell.addAhaSvc
async def mockaddsvc(self, name, info, network=None):
    if getattr(self, 'testerr', False):
        raise s_exc.SynErr(mesg='newp')
    return await realaddsvc(self, name, info, network=network)

class AhaTest(s_test.SynTest):
    aha_ctor = s_aha.AhaCell.anit

    async def test_lib_aha_mirrors(self):

        with self.getTestDir() as dirn:
            dir0 = s_common.gendir(dirn, 'aha0')
            dir1 = s_common.gendir(dirn, 'aha1')

            conf = {'nexslog:en': True}

            async with self.getTestAha(conf={'nexslog:en': True}, dirn=dir0) as aha0:
                user = await aha0.auth.addUser('reguser', passwd='secret')
                await user.setAdmin(True)

            s_tools_backup.backup(dir0, dir1)

            async with self.getTestAha(conf=conf, dirn=dir0) as aha0:
                upstream_url = aha0.getLocalUrl()

                mirrorconf = {
                    'nexslog:en': True,
                    'mirror': upstream_url,
                }

                async with self.getTestAha(conf=mirrorconf, dirn=dir1) as aha1:
                    # CA is nexus-fied
                    cabyts = await aha0.genCaCert('mirrorca')
                    await aha1.sync()
                    mirbyts = await aha1.genCaCert('mirrorca')
                    self.eq(cabyts, mirbyts)
                    iden = s_common.guid()
                    # Adding, downing, and removing service is also nexusified
                    info = {'urlinfo': {'host': '127.0.0.1', 'port': 8080,
                                        'scheme': 'tcp'},
                            'online': iden}
                    await aha0.addAhaSvc('test', info, network='example.net')
                    await aha1.sync()
                    mnfo = await aha1.getAhaSvc('test.example.net')
                    self.eq(mnfo.get('name'), 'test.example.net')

                    wait00 = aha0.waiter(1, 'aha:svcdown')
                    await aha0.setAhaSvcDown('test', iden, network='example.net')
                    self.len(1, await wait00.wait(timeout=6))
                    await aha1.sync()
                    mnfo = await aha1.getAhaSvc('test.example.net')
                    self.notin('online', mnfo)

                    await aha0.delAhaSvc('test', network='example.net')
                    await aha1.sync()
                    mnfo = await aha1.getAhaSvc('test.example.net')
                    self.none(mnfo)

    async def test_lib_aha_offon(self):
        with self.getTestDir() as dirn:
            cryo0_dirn = s_common.gendir(dirn, 'cryo0')
            conf = {'auth:passwd': 'secret'}
            async with self.getTestAha(conf=conf.copy(), dirn=dirn) as aha:
                host, port = await aha.dmon.listen('tcp://127.0.0.1:0')

                wait00 = aha.waiter(1, 'aha:svcadd')
                cryo_conf = {
                    'aha:name': '0.cryo.mynet',
                    'aha:admin': 'root@cryo.mynet',
                    'aha:registry': f'tcp://root:secret@127.0.0.1:{port}',
                    'dmon:listen': 'tcp://0.0.0.0:0/',
                }
                async with self.getTestCryo(dirn=cryo0_dirn, conf=cryo_conf.copy()) as cryo:
                    self.len(1, await wait00.wait(timeout=6))

                    svc = await aha.getAhaSvc('0.cryo.mynet')
                    linkiden = svc.get('svcinfo', {}).get('online')
                    self.nn(linkiden)

                    # Tear down the Aha cell.
                    await aha.__aexit__(None, None, None)

            async with self.getTestAha(conf=conf.copy(), dirn=dirn) as aha:
                wait01 = aha.waiter(1, 'aha:svcdown')
                await wait01.wait(timeout=6)
                svc = await aha.getAhaSvc('0.cryo.mynet')
                self.notin('online', svc.get('svcinfo'))

                # Try setting something down a second time
                await aha.setAhaSvcDown('0.cryo.mynet', linkiden, network=None)
                svc = await aha.getAhaSvc('0.cryo.mynet')
                self.notin('online', svc.get('svcinfo'))

    async def test_lib_aha(self):

        with self.raises(s_exc.NoSuchName):
            await s_telepath.getAhaProxy({})

        with self.raises(s_exc.NotReady):
            await s_telepath.getAhaProxy({'host': 'hehe.haha'})

        # We do inprocess reference counting for urls and clients.
        urls = ['newp://newp@newp', 'newp://newp@newp']
        info = await s_telepath.addAhaUrl(urls)
        self.eq(info.get('refs'), 1)
        # There is not yet a telepath client which is using these urls.
        self.none(info.get('client'))
        info = await s_telepath.addAhaUrl(urls)
        self.eq(info.get('refs'), 2)

        await s_telepath.delAhaUrl(urls)
        self.len(1, s_telepath.aha_clients)
        await s_telepath.delAhaUrl(urls)
        self.len(0, s_telepath.aha_clients)

        self.eq(0, await s_telepath.delAhaUrl('newp'))

        async with self.getTestAha() as aha:

            cryo0_dirn = s_common.gendir(aha.dirn, 'cryo0')

            host, port = await aha.dmon.listen('tcp://127.0.0.1:0')
            await aha.auth.rootuser.setPasswd('hehehaha')

            wait00 = aha.waiter(1, 'aha:svcadd')
            conf = {
                'aha:name': '0.cryo.mynet',
                'aha:leader': 'cryo.mynet',
                'aha:admin': 'root@cryo.mynet',
                'aha:registry': [f'tcp://root:hehehaha@127.0.0.1:{port}',
                                 f'tcp://root:hehehaha@127.0.0.1:{port}'],
                'dmon:listen': 'tcp://0.0.0.0:0/',
            }
            async with self.getTestCryo(dirn=cryo0_dirn, conf=conf) as cryo:

                await cryo.auth.rootuser.setPasswd('secret')

                ahaadmin = await cryo.auth.getUserByName('root@cryo.mynet')
                self.nn(ahaadmin)
                self.true(ahaadmin.isAdmin())

                await wait00.wait(timeout=2)

                with self.raises(s_exc.NoSuchName):
                    await s_telepath.getAhaProxy({'host': 'hehe.haha'})

                async with await s_telepath.openurl('aha://root:secret@cryo.mynet') as proxy:
                    self.nn(await proxy.getCellIden())

                with self.raises(s_exc.BadArg):
                    await cryo.ahaclient.waitready(timeout=2)
                    await cryo.ahaclient.modAhaSvcInfo('cryo.mynet', {'newp': 'newp'})

                async with await s_telepath.openurl('aha://root:secret@0.cryo.mynet') as proxy:
                    self.nn(await proxy.getCellIden())

                # force a reconnect...
                proxy = await cryo.ahaclient.proxy(timeout=2)
                await proxy.fini()

                async with await s_telepath.openurl('aha://root:secret@cryo.mynet') as proxy:
                    self.nn(await proxy.getCellIden())

                # force the service into passive mode...
                await cryo.setCellActive(False)

                with self.raises(s_exc.NoSuchName):
                    async with await s_telepath.openurl('aha://root:secret@cryo.mynet') as proxy:
                        pass

                async with await s_telepath.openurl('aha://root:secret@0.cryo.mynet') as proxy:
                    self.nn(await proxy.getCellIden())

                await cryo.setCellActive(True)

                async with await s_telepath.openurl('aha://root:secret@cryo.mynet') as proxy:
                    self.nn(await proxy.getCellIden())

                # some coverage edge cases...
                cryo.conf.pop('aha:leader', None)
                await cryo.setCellActive(False)

                # lock the aha:admin account so we can confirm it is unlocked upon restart
                # remove the admin flag from the account.
                self.false(ahaadmin.isLocked())
                await ahaadmin.setLocked(True, logged=False)
                self.true(ahaadmin.isLocked())
                # remove the admin status so we can confirm its an admin upon restart
                await ahaadmin.setAdmin(False, logged=False)
                self.false(ahaadmin.isAdmin())

            async with self.getTestCryo(dirn=cryo0_dirn, conf=conf) as cryo:
                ahaadmin = await cryo.auth.getUserByName('root@cryo.mynet')
                # And we should be unlocked and admin now
                self.false(ahaadmin.isLocked())
                self.true(ahaadmin.isAdmin())

            wait01 = aha.waiter(1, 'aha:svcadd')
            conf = {
                'aha:name': '0.cryo',
                'aha:leader': 'cryo',
                'aha:network': 'foo',
                'aha:registry': f'tcp://root:hehehaha@127.0.0.1:{port}',
                'dmon:listen': 'tcp://0.0.0.0:0/',
            }
            async with self.getTestCryo(conf=conf) as cryo:

                await cryo.auth.rootuser.setPasswd('secret')

                await wait01.wait(timeout=2)

                async with await s_telepath.openurl('aha://root:secret@cryo.foo') as proxy:
                    self.nn(await proxy.getCellIden())

                async with await s_telepath.openurl('aha://root:secret@0.cryo.foo') as proxy:
                    self.nn(await proxy.getCellIden())
                    await proxy.puts('hehe', ('hehe', 'haha'))

                async with await s_telepath.openurl('aha://root:secret@0.cryo.foo/*/hehe') as proxy:
                    self.nn(await proxy.iden())

                async with await s_telepath.openurl(f'tcp://root:hehehaha@127.0.0.1:{port}') as ahaproxy:
                    svcs = [x async for x in ahaproxy.getAhaSvcs('foo')]
                    self.len(2, svcs)
                    names = [s['name'] for s in svcs]
                    self.sorteq(('cryo.foo', '0.cryo.foo'), names)

                    self.none(await ahaproxy.getCaCert('vertex.link'))
                    cacert0 = await ahaproxy.genCaCert('vertex.link')
                    cacert1 = await ahaproxy.genCaCert('vertex.link')
                    self.nn(cacert0)
                    self.eq(cacert0, cacert1)
                    self.eq(cacert0, await ahaproxy.getCaCert('vertex.link'))

                    csrpem = cryo.certdir.genHostCsr('cryo.vertex.link').decode()

                    hostcert00 = await ahaproxy.signHostCsr(csrpem)
                    hostcert01 = await ahaproxy.signHostCsr(csrpem)

                    self.nn(hostcert00)
                    self.nn(hostcert01)
                    self.ne(hostcert00, hostcert01)

                    csrpem = cryo.certdir.genUserCsr('visi@vertex.link').decode()

                    usercert00 = await ahaproxy.signUserCsr(csrpem)
                    usercert01 = await ahaproxy.signUserCsr(csrpem)

                    self.nn(usercert00)
                    self.nn(usercert01)
                    self.ne(usercert00, usercert01)

            async with await s_telepath.openurl(f'tcp://root:hehehaha@127.0.0.1:{port}') as ahaproxy:
                await ahaproxy.delAhaSvc('cryo', network='foo')
                await ahaproxy.delAhaSvc('0.cryo', network='foo')
                self.none(await ahaproxy.getAhaSvc('cryo.foo'))
                self.none(await ahaproxy.getAhaSvc('0.cryo.foo'))
                self.len(2, [s async for s in ahaproxy.getAhaSvcs()])

                with self.raises(s_exc.BadArg):
                    info = {'urlinfo': {'host': '127.0.0.1', 'port': 8080, 'scheme': 'tcp'}}
                    await ahaproxy.addAhaSvc('newp', info, network=None)

        # The aha service can also be configured with a set of URLs that could represent itself.
        urls = ('cell://home0', 'cell://home1')
        conf = {'aha:urls': urls}
        async with self.getTestAha(conf=conf) as aha:
            async with aha.getLocalProxy() as ahaproxy:
                aurls = await ahaproxy.getAhaUrls()
                self.eq(urls, aurls)

    async def test_lib_aha_loadenv(self):

        with self.getTestDir() as dirn:

            async with self.getTestAha() as aha:
                host, port = await aha.dmon.listen('tcp://127.0.0.1:0')
                await aha.auth.rootuser.setPasswd('hehehaha')

                conf = {
                    'version': 1,
                    'aha:servers': [
                        f'tcp://root:hehehaha@127.0.0.1:{port}/',
                    ],
                }

                path = s_common.genpath(dirn, 'telepath.yaml')
                s_common.yamlsave(conf, path)

                # No clients have been loaded yet.
                with self.raises(s_exc.NotReady) as cm:
                    await s_telepath.openurl('aha://visi@foo.bar.com')
                self.eq(cm.exception.get('mesg'),
                        'No aha servers registered to lookup foo.bar.com')

                fini = await s_telepath.loadTeleEnv(path)

                # Should be one uninitialized aha client
                self.len(1, s_telepath.aha_clients)
                [info] = s_telepath.aha_clients.values()
                self.none(info.get('client'))

                with self.raises(s_exc.NoSuchName):
                    await s_telepath.openurl('aha://visi@foo.bar.com')

                # Connecting to an aha url should have initialized the client
                self.len(1, s_telepath.aha_clients)
                self.nn(info.get('client'))
                await fini()

    async def test_lib_aha_finid_cell(self):

        with self.getTestDir() as dirn:
            async with await self.aha_ctor(dirn) as aha:

                cryo0_dirn = s_common.gendir(aha.dirn, 'cryo0')

                host, port = await aha.dmon.listen('tcp://127.0.0.1:0')
                await aha.auth.rootuser.setPasswd('hehehaha')

                wait00 = aha.waiter(1, 'aha:svcadd')
                conf = {
                    'aha:name': '0.cryo.mynet',
                    'aha:admin': 'root@cryo.mynet',
                    'aha:registry': [f'tcp://root:hehehaha@127.0.0.1:{port}',
                                     f'tcp://root:hehehaha@127.0.0.1:{port}'],
                    'dmon:listen': 'tcp://0.0.0.0:0/',
                }
                async with self.getTestCryo(dirn=cryo0_dirn, conf=conf) as cryo:

                    await cryo.auth.rootuser.setPasswd('secret')

                    ahaadmin = await cryo.auth.getUserByName('root@cryo.mynet')
                    self.nn(ahaadmin)
                    self.true(ahaadmin.isAdmin())

                    await wait00.wait(timeout=2)

                    async with await s_telepath.openurl('aha://root:secret@0.cryo.mynet') as proxy:
                        self.nn(await proxy.getCellIden())

                    await aha.fini()

                    with self.raises(s_exc.IsFini):

                        async with await s_telepath.openurl('aha://root:secret@0.cryo.mynet') as proxy:
                            self.fail('Should never reach a connection.')

    async def test_lib_aha_onlink_fail(self):

        with self.getTestDir() as dirn:

            with mock.patch('synapse.lib.aha.AhaCell.addAhaSvc', mockaddsvc):

                async with await self.aha_ctor(dirn) as aha:

                    cryo0_dirn = s_common.gendir(aha.dirn, 'cryo0')

                    host, port = await aha.dmon.listen('tcp://127.0.0.1:0')
                    await aha.auth.rootuser.setPasswd('secret')

                    aha.testerr = True

                    wait00 = aha.waiter(1, 'aha:svcadd')
                    conf = {
                        'aha:name': '0.cryo.mynet',
                        'aha:admin': 'root@cryo.mynet',
                        'aha:registry': f'tcp://root:secret@127.0.0.1:{port}',
                        'dmon:listen': 'tcp://0.0.0.0:0/',
                    }
                    async with self.getTestCryo(dirn=cryo0_dirn, conf=conf) as cryo:

                        await cryo.auth.rootuser.setPasswd('secret')

                        self.none(await wait00.wait(timeout=2))

                        svc = await aha.getAhaSvc('0.cryo.mynet')
                        self.none(svc)

                        wait01 = aha.waiter(1, 'aha:svcadd')
                        aha.testerr = False

                        self.nn(await wait01.wait(timeout=2))

                        svc = await aha.getAhaSvc('0.cryo.mynet')
                        self.nn(svc)
                        self.nn(svc.get('svcinfo', {}).get('online'))

                        async with await s_telepath.openurl('aha://root:secret@0.cryo.mynet') as proxy:
                            self.nn(await proxy.getCellIden())

    async def test_lib_aha_bootstrap(self):

        with self.getTestDir() as dirn:
            certdirn = s_common.gendir('certdir')
            with self.getTestCertDir(certdirn):

                conf = {
                    'aha:name': 'aha',
                    'aha:admin': 'root@do.vertex.link',
                    'aha:network': 'do.vertex.link',
                }

                async with await s_aha.AhaCell.anit(dirn, conf=conf) as aha:
                    self.true(os.path.isfile(os.path.join(dirn, 'certs', 'cas', 'do.vertex.link.crt')))
                    self.true(os.path.isfile(os.path.join(dirn, 'certs', 'cas', 'do.vertex.link.key')))
                    self.true(os.path.isfile(os.path.join(dirn, 'certs', 'hosts', 'aha.do.vertex.link.crt')))
                    self.true(os.path.isfile(os.path.join(dirn, 'certs', 'hosts', 'aha.do.vertex.link.key')))
                    self.true(os.path.isfile(os.path.join(dirn, 'certs', 'users', 'root@do.vertex.link.crt')))
                    self.true(os.path.isfile(os.path.join(dirn, 'certs', 'users', 'root@do.vertex.link.key')))

                    host, port = await aha.dmon.listen('ssl://127.0.0.1:0?hostname=aha.do.vertex.link&ca=do.vertex.link')

                    async with await s_telepath.openurl(f'ssl://root@127.0.0.1:{port}?hostname=aha.do.vertex.link') as proxy:
                        await proxy.getCellInfo()

    async def test_lib_aha_noconf(self):

        with self.getTestDir() as dirn:

            async with await self.aha_ctor(dirn) as aha:

                with self.raises(s_exc.NeedConfValu):
                    await aha.addAhaSvcProv('hehe')

                aha.conf['aha:urls'] = 'tcp://127.0.0.1:0/'

                with self.raises(s_exc.NeedConfValu):
                    await aha.addAhaSvcProv('hehe')

                with self.raises(s_exc.NeedConfValu):
                    await aha.addAhaUserEnroll('hehe')

                aha.conf['provision:listen'] = 'tcp://127.0.0.1:27272'

                with self.raises(s_exc.NeedConfValu):
                    await aha.addAhaSvcProv('hehe')

                with self.raises(s_exc.NeedConfValu):
                    await aha.addAhaUserEnroll('hehe')

                aha.conf['aha:network'] = 'haha'
                await aha.addAhaSvcProv('hehe')

    async def test_lib_aha_provision(self):

        with self.getTestDir() as dirn:

            conf = {
                'aha:name': 'aha',
                'aha:network': 'loop.vertex.link',
                'provision:listen': 'ssl://aha.loop.vertex.link:0'
            }
            async with await self.aha_ctor(dirn, conf=conf) as aha:

                addr, port = aha.provdmon.addr
                # update the config to reflect the dynamically bound port
                aha.conf['provision:listen'] = f'ssl://aha.loop.vertex.link:{port}'

                # do this config ex-post-facto due to port binding...
                host, ahaport = await aha.dmon.listen('ssl://0.0.0.0:0?hostname=aha.loop.vertex.link&ca=loop.vertex.link')
                aha.conf['aha:urls'] = f'ssl://aha.loop.vertex.link:{ahaport}'

                url = aha.getLocalUrl()

                outp = s_output.OutPutStr()
                await s_tools_provision_service.main(('--url', aha.getLocalUrl(), 'foobar'), outp=outp)
                self.isin('one-time use URL: ', str(outp))

                provurl = str(outp).split(':', 1)[1].strip()

                async with await s_telepath.openurl(provurl) as prov:
                    provinfo = await prov.getProvInfo()
                    self.isinstance(provinfo, dict)
                    conf = provinfo.get('conf')
                    # Default https port is not set; dmon is port 0
                    self.notin('https:port', conf)
                    dmon_listen = conf.get('dmon:listen')
                    parts = s_telepath.chopurl(dmon_listen)
                    self.eq(parts.get('port'), 0)
                    self.nn(await prov.getCaCert())

                with self.raises(s_exc.NoSuchName):
                    await s_telepath.openurl(provurl)

                async with aha.getLocalProxy() as proxy:
                    onebork = await proxy.addAhaSvcProv('bork')
                    await proxy.delAhaSvcProv(onebork)

                    onenewp = await proxy.addAhaSvcProv('newp')
                    async with await s_telepath.openurl(onenewp) as provproxy:

                        byts = aha.certdir.genHostCsr('lalala')
                        with self.raises(s_exc.BadArg):
                            await provproxy.signHostCsr(byts)

                        byts = aha.certdir.genUserCsr('lalala')
                        with self.raises(s_exc.BadArg):
                            await provproxy.signUserCsr(byts)

                    onebork = await proxy.addAhaUserEnroll('bork00')
                    await proxy.delAhaUserEnroll(onebork)

                    onebork = await proxy.addAhaUserEnroll('bork01')
                    async with await s_telepath.openurl(onebork) as provproxy:

                        byts = aha.certdir.genUserCsr('zipzop')
                        with self.raises(s_exc.BadArg):
                            await provproxy.signUserCsr(byts)

                onetime = await aha.addAhaSvcProv('00.axon')

                axonpath = s_common.gendir(dirn, 'axon')
                axonconf = {
                    'aha:provision': onetime,
                }
                s_common.yamlsave(axonconf, axonpath, 'cell.yaml')

                argv = (axonpath, '--auth-passwd', 'rootbeer')
                async with await s_axon.Axon.initFromArgv(argv) as axon:

                    # opts were copied through successfully
                    self.true(await axon.auth.rootuser.tryPasswd('rootbeer'))

                    # test that nobody set aha:admin
                    self.none(await axon.auth.getUserByName('root@loop.vertex.link'))
                    self.none(await axon.auth.getUserByName('axon@loop.vertex.link'))

                    self.true(os.path.isfile(s_common.genpath(axon.dirn, 'prov.done')))
                    self.true(os.path.isfile(s_common.genpath(axon.dirn, 'certs', 'cas', 'loop.vertex.link.crt')))
                    self.true(os.path.isfile(s_common.genpath(axon.dirn, 'certs', 'hosts', '00.axon.loop.vertex.link.crt')))
                    self.true(os.path.isfile(s_common.genpath(axon.dirn, 'certs', 'hosts', '00.axon.loop.vertex.link.key')))
                    self.true(os.path.isfile(s_common.genpath(axon.dirn, 'certs', 'users', 'root@loop.vertex.link.crt')))
                    self.true(os.path.isfile(s_common.genpath(axon.dirn, 'certs', 'users', 'root@loop.vertex.link.key')))

                    yamlconf = s_common.yamlload(axon.dirn, 'cell.yaml')
                    self.eq('axon', yamlconf.get('aha:leader'))
                    self.eq('00.axon', yamlconf.get('aha:name'))
                    self.eq('loop.vertex.link', yamlconf.get('aha:network'))
                    self.none(yamlconf.get('aha:admin'))
                    self.eq((f'ssl://root@aha.loop.vertex.link:{ahaport}',), yamlconf.get('aha:registry'))
                    self.eq(f'ssl://0.0.0.0:0?hostname=00.axon.loop.vertex.link&ca=loop.vertex.link', yamlconf.get('dmon:listen'))

                    await axon.addUser('visi')

                    outp = s_output.OutPutStr()
                    await s_tools_provision_user.main(('--url', aha.getLocalUrl(), 'visi'), outp=outp)
                    self.isin('one-time use URL:', str(outp))

                    provurl = str(outp).split(':', 1)[1].strip()
                    with self.getTestDir() as syndir:
                        with mock.patch('synapse.common.syndir', syndir):

                            outp = s_output.OutPutStr()
                            await s_tools_enroll.main((provurl,), outp=outp)

                            self.true(os.path.isfile(s_common.genpath(syndir, 'certs', 'cas', 'loop.vertex.link.crt')))
                            self.true(os.path.isfile(s_common.genpath(syndir, 'certs', 'users', 'visi@loop.vertex.link.crt')))
                            self.true(os.path.isfile(s_common.genpath(syndir, 'certs', 'users', 'visi@loop.vertex.link.key')))

                            teleyaml = s_common.yamlload(syndir, 'telepath.yaml')
                            self.eq(teleyaml.get('version'), 1)
                            self.eq(teleyaml.get('aha:servers'), (f'ssl://visi@aha.loop.vertex.link:{ahaport}',))

                    outp = s_output.OutPutStr()
                    await s_tools_provision_user.main(('--url', aha.getLocalUrl(), 'visi'), outp=outp)
                    self.isin('Need --again', str(outp))

                    outp = s_output.OutPutStr()
                    await s_tools_provision_user.main(('--url', aha.getLocalUrl(), '--again', 'visi'), outp=outp)
                    self.isin('one-time use URL:', str(outp))

                onetime = await aha.addAhaSvcProv('00.axon')
                axonconf = {
                    'aha:provision': onetime,
                }
                s_common.yamlsave(axonconf, axonpath, 'cell.yaml')

                # Populate data in the overrides file that will be removed from the
                # provisioning data
                overconf = {
                    'dmon:listen': 'tcp://0.0.0.0:0',  # This is removed
                    'nexslog:async': True,  # just set as a demonstrative value
                }
                s_common.yamlsave(overconf, axonpath, 'cell.mods.yaml')

                # force a re-provision... (because the providen is different)
                with self.getAsyncLoggerStream('synapse.lib.cell',
                                               'Provisioning axon from AHA service') as stream:
                    async with await s_axon.Axon.initFromArgv((axonpath,)) as axon:
                        self.true(await stream.wait(6))
                        self.ne(axon.conf.get('dmon:listen'),
                                'tcp://0.0.0.0:0')
                overconf2 = s_common.yamlload(axonpath, 'cell.mods.yaml')
                self.eq(overconf2, {'nexslog:async': True})

                # tests startup logic that recognizes it's already done
                with self.getAsyncLoggerStream('synapse.lib.cell', ) as stream:
                    async with await s_axon.Axon.initFromArgv((axonpath,)) as axon:
                        pass
                    stream.seek(0)
                    self.notin('Provisioning axon from AHA service', stream.read())

                async with await s_axon.Axon.initFromArgv((axonpath,)) as axon:
                    # testing second run...
                    pass

                # Ensure we can provision a service on a given listening ports
                with self.raises(AssertionError):
                    await s_tools_provision_service.main(('--url', aha.getLocalUrl(), 'bazfaz', '--dmon-port', '123456'),
                                                         outp=outp)

                with self.raises(AssertionError):
                    await s_tools_provision_service.main(('--url', aha.getLocalUrl(), 'bazfaz', '--https-port', '123456'),
                                                         outp=outp)
                outp = s_output.OutPutStr()
                argv = ('--url', aha.getLocalUrl(), 'bazfaz', '--dmon-port', '1234', '--https-port', '443')
                await s_tools_provision_service.main(argv, outp=outp)
                self.isin('one-time use URL: ', str(outp))
                provurl = str(outp).split(':', 1)[1].strip()
                async with await s_telepath.openurl(provurl) as proxy:
                    provconf = await proxy.getProvInfo()
                    conf = provconf.get('conf')
                    dmon_listen = conf.get('dmon:listen')
                    parts = s_telepath.chopurl(dmon_listen)
                    self.eq(parts.get('port'), 1234)
                    https_port = conf.get('https:port')
                    self.eq(https_port, 443)

    async def test_aha_provmirror(self):

        with self.getTestDir() as dirn:

            dirn_aha00 = s_common.gendir(dirn, 'aha00')
            dirn_aha01 = s_common.gendir(dirn, 'aha01')
            dirn_certs = s_common.gendir(dirn, 'certdir')

            with self.getTestCertDir(dirn_certs) as certdir:

                conf_aha00 = {
                    'aha:network': 'loop.vertex.link',
                    'provision:listen': 'ssl://00.aha.loop.vertex.link:0',
                    'dmon:listen': 'ssl://0.0.0.0:0?hostname=00.aha.loop.vertex.link&ca=loop.vertex.link',

                    # changes to deployment guide for mirroring:
                    'aha:name': '00.aha',
                    'aha:admin': 'root@loop.vertex.link',
                    'aha:leader': 'aha',

                    # easiest path is probably to setup aha:urls and aha:registry upfront
                    # otherwise would need a nexus-safe way to update these as new mirrors get provisioned
                    # these are not set in this test b/c of dynamic port binding
                    # 'aha:urls': [
                    #     'ssl://00.aha.loop.vertex.link:0',
                    #     'ssl://01.aha.loop.vertex.link:0',
                    # ],
                    # 'aha:registry': [
                    #     'ssl://root@00.aha.loop.vertex.link:0',
                    #     'ssl://root@01.aha.loop.vertex.link:0',
                    # ],
                }
                async with self.getTestAha(conf=conf_aha00, dirn=dirn_aha00) as aha00:

                    # updates for dynamic port binding
                    ahaport00 = aha00.sockaddr[1]
                    aha00.conf['dmon:listen'] = f'ssl://0.0.0.0:{ahaport00}?hostname=00.aha.loop.vertex.link&ca=loop.vertex.link'
                    aha00.conf['provision:listen'] = f'ssl://00.aha.loop.vertex.link:{aha00.provdmon.addr[1]}'

                    # mock setting these upfront although mirrors would be included here too
                    aha00.conf['aha:urls'] = [f'ssl://00.aha.loop.vertex.link:{ahaport00}']
                    aha00.conf['aha:registry'] = [f'ssl://root@00.aha.loop.vertex.link:{ahaport00}']

                    # self-provision aha00
                    # needs to happen after initial boot so the cell is up
                    # alternatively could treat registering w/self when the leader specially
                    wait00 = aha00.waiter(2, 'aha:svcadd')
                    await aha00._initAhaRegistry()
                    await aha00._initAhaService()
                    self.len(2, await wait00.wait(timeout=6))
                    infos00 = [info async for info in aha00.getAhaSvcs()]
                    self.len(2, infos00)

                    async with await s_telepath.openurl('aha://root@00.aha.loop.vertex.link') as proxy:
                        self.nn(await proxy.getCellIden())
                    async with await s_telepath.openurl('aha://root@aha.loop.vertex.link') as proxy:
                        self.nn(await proxy.getCellIden())

                    # provision the aha mirror
                    provinfo = {'mirror': 'aha'}
                    provurl = await aha00.addAhaSvcProv('01.aha', provinfo=provinfo)
                    conf_aha01 = {'aha:provision': provurl}
                    wait00 = aha00.waiter(1, 'aha:svcadd')
                    async with self.getTestAha(conf=conf_aha01, dirn=dirn_aha01) as aha01:
                        self.len(1, await wait00.wait(timeout=6))
                        infos01 = [info async for info in aha00.getAhaSvcs()]
                        self.len(3, infos01)
                        await aha01.sync()

                        # aha:urls should be passed to the provisioned mirror
                        # but either way bootstrap here since not set in initial conf
                        # due to dynamic port binding
                        ahaport01 = [info['svcinfo']['urlinfo']['port'] for info in infos01 if info['svcname'] == '01.aha'][0]
                        aha01.conf['aha:urls'] = [
                            f'ssl://00.aha.loop.vertex.link:{ahaport00}',
                            f'ssl://01.aha.loop.vertex.link:{ahaport01}',
                        ]
                        aha01.conf['aha:registry'] = [
                            f'ssl://root@00.aha.loop.vertex.link:{ahaport00}',
                            f'ssl://root@01.aha.loop.vertex.link:{ahaport01}',
                        ]
                        await aha01.ahaclient.fini()
                        await aha01._initAhaRegistry()
                        await aha01._initAhaService()

                        # update the urls for the leader too
                        # again these would be defined up front
                        aha00.conf['aha:urls'] = [
                            f'ssl://00.aha.loop.vertex.link:{ahaport00}',
                            f'ssl://01.aha.loop.vertex.link:{ahaport01}',
                        ]
                        aha00.conf['aha:registry'] = [
                            f'ssl://root@00.aha.loop.vertex.link:{ahaport00}',
                            f'ssl://root@01.aha.loop.vertex.link:{ahaport01}',
                        ]
                        await aha00.ahaclient.fini()
                        await aha00._initAhaRegistry()
                        await aha00._initAhaService()

                        await asyncio.sleep(2)  # replace this w/a waiter

                        self.true(all([info['svcinfo']['online'] async for info in aha00.getAhaSvcs()]))
                        self.true(all([info['svcinfo']['online'] async for info in aha01.getAhaSvcs()]))

                        # provision:listen should be passed down to the mirror
                        provlisten = f'ssl://01.aha.loop.vertex.link:0'
                        aha01.provdmon = await s_aha.ProvDmon.anit(aha01)
                        aha01.onfini(aha01.provdmon)
                        await aha01.provdmon.listen(provlisten)
                        addr, port = aha01.provdmon.addr
                        aha01.conf['provision:listen'] = f'ssl://01.aha.loop.vertex.link:{port}'

                        # provision a core from the aha leader
                        provurl = await aha00.addAhaSvcProv('00.acore')
                        coreconf = {'aha:provision': provurl}
                        wait00 = aha00.waiter(1, 'aha:svcadd')
                        async with self.getTestCore(conf=coreconf) as core00:
                            self.len(1, await wait00.wait(timeout=2))
                            await core00.nodes('[inet:ipv4=0]')
                            await aha01.sync()
                            self.nn(await aha01.getAhaSvc('00.acore...'))
                            self.nn(await aha01.getAhaSvc('acore...'))

                        # provision from the follower
                        provurl = await aha01.addAhaSvcProv('00.bcore')
                        coreconf = {'aha:provision': provurl}
                        wait00 = aha01.waiter(1, 'aha:svcadd')
                        async with self.getTestCore(conf=coreconf) as core01:
                            self.len(1, await wait00.wait(timeout=2))
                            await core01.nodes('[inet:ipv4=1]')
                            await aha01.sync()
                            self.nn(await aha00.getAhaSvc('00.bcore...'))
                            self.nn(await aha00.getAhaSvc('bcore...'))

                        # promote the follower
                        # await aha01.promote(graceful=True)
                        # gets stuck at _tellAhaReady() -> modAhaSvcInfo() since aha00 has a nexus lock
                        # at this point aha00 is still active and aha01 is not active

                        # semi-graceful promotion
                        # the main change is for the leader to go inactive before applying the lock
                        await aha00.setCellActive(False)
                        async with aha00.nexsroot.applylock:
                            indx = await aha00.getNexsIndx()
                            self.true(await aha01.waitNexsOffs(indx - 1, timeout=2))

                            aha01.modCellConf({'mirror': None})
                            aha00.modCellConf({'mirror': 'aha://root@aha.loop.vertex.link'})

                            # the new leader should be able to itself
                            # that its active and ready
                            await aha01.nexsroot.promote()
                            await aha01.setCellActive(True)

                            # at this point the new leader should be ready
                            # it will fail to connect to self, but can connect to the new leader
                            # since it has both urls in its registry
                            await asyncio.sleep(2)  # replace w/waiter
                            await aha00.nexsroot.startup()

                        await asyncio.sleep(2)  # replace w/waiter

                        info = await aha01.getAhaSvc('aha...')
                        self.eq('01.aha.loop.vertex.link', info['svcinfo']['urlinfo']['hostname'])
                        self.nn(info['svcinfo']['online'])

                        info00 = await aha01.getAhaSvc('00.aha...')
                        self.nn(info00['svcinfo']['online'])

                        info01 = await aha01.getAhaSvc('01.aha...')
                        self.nn(info01['svcinfo']['online'])

                        await aha00.sync()

                        # tl;dr on possible changes
                        # - if configured, the aha leader needs to bootstrap itself as an aha svc post-startup
                        # - provision:listen and aha:urls needs to get passed to a provisioned aha mirror
                        # - graceful promotion needs special handling to go inactive before actual handoff/promotion

                        # notes on deployment guide (assuming changes noted above)
                        # - define how many aha's you want, and set the urls for aha:urls/aha:registry
                        #       - could automagically set aha:registry if aha:urls provided
                        # - all *.aha fqdns need to be resolvable so provision urls work
                        # - aha mirrors don't have to be setup before everything else, but probably makes sense to do so
                        # - doc promotion caveats
                        # - even without being mirrored probably makes sense to move guide to use 00.aha for future self

    async def test_aha_httpapi(self):
        with self.getTestDir() as dirn:

            conf = {
                'aha:name': 'aha',
                'aha:network': 'loop.vertex.link',
                'provision:listen': 'ssl://aha.loop.vertex.link:0'
            }
            async with await self.aha_ctor(dirn, conf=conf) as aha:

                await aha.auth.rootuser.setPasswd('secret')

                addr, port = aha.provdmon.addr
                # update the config to reflect the dynamically bound port
                aha.conf['provision:listen'] = f'ssl://aha.loop.vertex.link:{port}'

                # do this config ex-post-facto due to port binding...
                host, ahaport = await aha.dmon.listen('ssl://0.0.0.0:0?hostname=aha.loop.vertex.link&ca=loop.vertex.link')
                aha.conf['aha:urls'] = f'ssl://aha.loop.vertex.link:{ahaport}'

                host, httpsport = await aha.addHttpsPort(0)
                url = f'https://localhost:{httpsport}/api/v1/aha/provision/service'

                async with self.getHttpSess(auth=('root', 'secret'), port=httpsport) as sess:

                    # Simple request works
                    async with sess.post(url, json={'name': '00.foosvc'}) as resp:
                        info = await resp.json()
                        self.eq(info.get('status'), 'ok')
                        result = info.get('result')
                        provurl = result.get('url')

                    async with await s_telepath.openurl(provurl) as prox:
                        provconf = await prox.getProvInfo()
                        self.isin('iden', provconf)
                        conf = provconf.get('conf')
                        self.eq(conf.get('aha:user'), 'root')
                        dmon_listen = conf.get('dmon:listen')
                        parts = s_telepath.chopurl(dmon_listen)
                        self.eq(parts.get('port'), 0)
                        self.none(conf.get('https:port'))

                    # Full api works as well
                    data = {'name': '01.foosvc',
                            'provinfo': {
                                'dmon:port': 12345,
                                'https:port': 8443,
                                'mirror': 'foosvc',
                                'conf': {
                                    'aha:user': 'test',
                                }
                            }
                    }
                    async with sess.post(url, json=data) as resp:
                        info = await resp.json()
                        self.eq(info.get('status'), 'ok')
                        result = info.get('result')
                        provurl = result.get('url')
                    async with await s_telepath.openurl(provurl) as prox:
                        provconf = await prox.getProvInfo()
                        conf = provconf.get('conf')
                        self.eq(conf.get('aha:user'), 'test')
                        dmon_listen = conf.get('dmon:listen')
                        parts = s_telepath.chopurl(dmon_listen)
                        self.eq(parts.get('port'), 12345)
                        self.eq(conf.get('https:port'), 8443)

                    # Sad path
                    async with sess.post(url) as resp:
                        info = await resp.json()
                        self.eq(info.get('status'), 'err')
                        self.eq(info.get('code'), 'SchemaViolation')
                    async with sess.post(url, json={}) as resp:
                        info = await resp.json()
                        self.eq(info.get('status'), 'err')
                        self.eq(info.get('code'), 'SchemaViolation')
                    async with sess.post(url, json={'name': 1234}) as resp:
                        info = await resp.json()
                        self.eq(info.get('status'), 'err')
                        self.eq(info.get('code'), 'SchemaViolation')
                    async with sess.post(url, json={'name': ''}) as resp:
                        info = await resp.json()
                        self.eq(info.get('status'), 'err')
                        self.eq(info.get('code'), 'SchemaViolation')
                    async with sess.post(url, json={'name': '00.newp', 'provinfo': 5309}) as resp:
                        info = await resp.json()
                        self.eq(info.get('status'), 'err')
                        self.eq(info.get('code'), 'SchemaViolation')
                    async with sess.post(url, json={'name': '00.newp', 'provinfo': {'dmon:port': -1}}) as resp:
                        info = await resp.json()
                        self.eq(info.get('status'), 'err')
                        self.eq(info.get('code'), 'SchemaViolation')

                    # Break the Aha cell - not will provision after this.
                    _network = aha.conf.pop('aha:network')
                    async with sess.post(url, json={'name': '00.newp'}) as resp:
                        info = await resp.json()
                        self.eq(info.get('status'), 'err')
                        self.eq(info.get('code'), 'NeedConfValu')

                # Not an admin
                await aha.addUser('lowuser', passwd='lowuser')
                async with self.getHttpSess(auth=('lowuser', 'lowuser'), port=httpsport) as sess:

                    async with sess.post(url, json={'name': '00.newp'}) as resp:
                        info = await resp.json()
                        self.eq(info.get('status'), 'err')
                        self.eq(info.get('code'), 'AuthDeny')
