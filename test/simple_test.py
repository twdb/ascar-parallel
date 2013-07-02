from ascar_parallel import StartCluster


def test_simple_map():
	serial_result = map(lambda x:x**10, range(32))
	parallel_result = None

	with StartCluster(8) as lview:
		parallel_result = map(lambda x:x**10, range(32))

	assert serial_result == parallel_result