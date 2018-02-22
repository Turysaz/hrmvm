# Copyright (c) Turysaz 2018
# This file is part of the HRMVM toolkit
# HRMVM is free software. See LICENSE file for further information

test:
	python -m unittest -v

clean:
	find . | grep "__pycache__" | xargs rm -rfv
