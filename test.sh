#!/bin/sh

function separator() 
{
	echo -e "\n======================================================================\n" 
}

pushd Logger > /dev/null
	python test_logger.py -vb
	separator
	python mtest_logger.py
popd > /dev/null
