from IPsReaper.reaper import IPReaper

rp = IPReaper(proxy=None)
rp.run_reaper()
ips_catch_lib = rp.get_ips_from_cache()
rp.test_ips(ips_catch_lib)
