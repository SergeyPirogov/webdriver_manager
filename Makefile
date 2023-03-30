.PHONY: docs test unittest xdisttest negatest package clean

PROJ_DIR := ${CURDIR}

DOC_DIR        := ${PROJ_DIR}/docs
TEST_DIR       := ${PROJ_DIR}/tests
TEST_XDIST_DIR := ${PROJ_DIR}/tests_xdist
TEST_NEGA_DIR  := ${PROJ_DIR}/tests_negative
SRC_DIR        := ${PROJ_DIR}/webdriver_manager

RANGE_DIR        ?= .
RANGE_TEST_DIR   := ${TEST_DIR}/${RANGE_DIR}
RANGE_TEST_XDIST := ${TEST_XDIST_DIR}/${RANGE_DIR}
RANGE_TEST_NEGA  := ${TEST_NEGA_DIR}/${RANGE_DIR}
RANGE_SRC_DIR    := ${SRC_DIR}/${RANGE_DIR}


COV_TYPES ?= xml term-missing

package:
	python -m build --sdist --wheel --outdir dist/

clean:
	rm -rf dist

test: unittest

unittest:
	pytest "${RANGE_TEST_DIR}" -sv \
		$(shell for type in ${COV_TYPES}; do echo "--cov-report=$$type"; done) \
		--cov="${RANGE_SRC_DIR}" \
		$(if ${MIN_COVERAGE},--cov-fail-under=${MIN_COVERAGE},) \
		$(if ${WORKERS},-n ${WORKERS},)

xdisttest:
	pytest "${RANGE_TEST_XDIST}" -sv \
		$(shell for type in ${COV_TYPES}; do echo "--cov-report=$$type"; done) \
		--cov="${RANGE_SRC_DIR}" \
		$(if ${MIN_COVERAGE},--cov-fail-under=${MIN_COVERAGE},) \
		$(if ${WORKERS},-n ${WORKERS},)

negatest:
	pytest "${RANGE_TEST_NEGA}" -sv \
		$(shell for type in ${COV_TYPES}; do echo "--cov-report=$$type"; done) \
		--cov="${RANGE_SRC_DIR}" \
		$(if ${MIN_COVERAGE},--cov-fail-under=${MIN_COVERAGE},) \
		$(if ${WORKERS},-n ${WORKERS},)

docs:
	$(MAKE) -C "${DOC_DIR}" build
pdocs:
	$(MAKE) -C "${DOC_DIR}" prod
