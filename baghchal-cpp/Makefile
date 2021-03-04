#
# Generic gcc/llvm c++ compiler wrapper for make in osx/linux/wsl
# this is a fairly complex makefile, but it is made to
#
#    Be fairly generic, so you probably only want to change flags
#    Allow the use of google test and google mock library in unit tests.
#
#    For your code:
#
#       Your header (.h) files should be in include
#       Your source (.cpp) files should be in src
#       src/main_xxxx.cpp is the main program for bin/xxxx
#       src/test_xxxx.cpp is the test program for bin/test_xxxx
#
#    You may want to change CXXFLAGS for other compile time options
#    Always rebuild everything after a flag change:
#
#       make clean all
#
#    Typical targets:
#
#	make bin/hello
#       make bin/test_hello
#       make clean
#       make all
#       make tests
#       make mains

# c++ compile flags
CXXFLAGS=-pthread -Iinclude -g -O2 -std=c++14 -fPIC
CFLAGS=-pthread -Iinclude -g -O2 -std=c++14 -fPIC

include Makefile.googletest

# all not-main and not-test source files in the src folder
CXX_PARTS=$(shell find src -name '*.cpp' -and -not \( -name '.*' -or -name 'main_*' -or -name 'test_*' \) )
C_PARTS=$(shell find src -name '*.c' -and -not \( -name '.*' -or -name 'main_*' -or -name 'test_*' \) )

# src/XXXX.cpp -> tmp/XXXX.cpp.o object files
CXX_OBJ_PARTS=$(patsubst src/%.cpp,tmp/%.cpp.o,$(CXX_PARTS))
C_OBJ_PARTS=$(patsubst src/%.c,tmp/%.c.o,$(C_PARTS))

# program main source files in src
CXX_MAINS=$(shell find src -name 'main_*.cpp')
C_MAINS=$(shell find src -name 'main_*.c')

# src/main_XXXX.cpp -> bin/XXXX executables
CXX_EXE_MAINS=$(patsubst src/main_%.cpp,bin/%,$(CXX_MAINS))
C_EXE_MAINS=$(patsubst src/main_%.c,bin/%,$(C_MAINS))

ALL += $(CXX_EXE_MAINS) 
ALL += $(C_EXE_MAINS)

# test source files in src
CXX_TESTS=$(shell find src -name 'test_*.cpp')
C_TESTS=$(shell find src -name 'test_*.c')

# src/test_XXXX.cpp -> bin/test_XXXX test executables
CXX_EXE_TESTS=$(patsubst src/test_%.cpp,bin/test_%,$(CXX_TESTS))
C_EXE_TESTS=$(patsubst src/test_%.c,bin/test_%,$(C_TESTS))

ALL += $(CXX_EXE_TESTS)
ALL += $(C_EXE_TESTS)

.PHONY: all
all : cxx_mains c_mains cxx_tests c_tests

.PHONY: cxx_mains
cxx_mains : $(CXX_EXE_MAINS)
.PHONY: c_mains
c_mains : $(C_EXE_MAINS)

.PHONY: cxx_tests
cxx_tests : googletest $(CXX_EXE_TESTS)
.PHONY: tests
c_tests : googletest $(C_EXE_TESTS)

.PHONY: clean
clean :
	/bin/rm -rf tmp/* bin/* lib/*.so
	find . \( -name '*~' -or -name '*#' -or -name '.#*' \) -print0 | xargs -0 /bin/rm -rf

# use compiler to automatically discover #include - dependencies... for cpp test
tmp/test_%.cpp.d: src/test_%.cpp
	mkdir -p `dirname $@`
	$(CXX) $(CXXFLAGS) $(GOOGLE_TEST_FLAGS) -MM -MT '$(patsubst src/%.cpp,tmp/%.cpp.o,$<)' $< > $@

# use compiler to automatically discover #include - dependencies... for c test
tmp/test_%.c.d: src/test_%.c
	mkdir -p `dirname $@`
	$(CC) $(CFLAGS) $(GOOGLE_TEST_FLAGS) -MM -MT '$(patsubst src/%.c,tmp/%.c.o,$<)' $< > $@

# use compiler to automatically discover #include - dependencies...
tmp/%.cpp.d: src/%.cpp
	mkdir -p `dirname $@`
	$(CXX) $(CXXFLAGS) -MM -MT '$(patsubst src/%.cpp,tmp/%.cpp.o,$<)' $< > $@

# use compiler to automatically discover #include - dependencies...
tmp/%.c.d: src/%.c
	mkdir -p `dirname $@`
	$(CC) $(CFLAGS) -MM -MT '$(patsubst src/%.c,tmp/%.c.o,$<)' $< > $@

# use (and maybe update) dependency rules unless I am cleaning or makeing googletests
ifneq (clean,$(MAKECMDGOALS))
ifneq (googletest,$(MAKECMDGOALS))
-include $(patsubst src/%.cpp,tmp/%.cpp.d,$(CXX_PARTS) $(CXX_MAINS) $(CXX_TESTS))
-include $(patsubst src/%.c,tmp/%.c.d,$(C_PARTS) $(C_MAINS) $(C_TESTS))
endif
endif

# generic compile a c++ test file rule
tmp/test_%.cpp.o: src/test_%.cpp
	mkdir -p `dirname $@`
	$(CXX) $(CXXFLAGS) $(GOOGLE_TEST_FLAGS) -c -o $@ $<

# generic compile a c test file rule
tmp/test_%.c.o: src/test_%.c
	mkdir -p `dirname $@`
	$(CC) $(CFLAGS) $(GOOGLE_TEST_FLAGS) -c -o $@ $<

# generic compile a c++ source file rule
tmp/%.cpp.o: src/%.cpp
	mkdir -p `dirname $@`
	$(CXX) $(CXXFLAGS) -c -o $@ $<

# generic compile a c source file rule
tmp/%.c.o: src/%.c
	mkdir -p `dirname $@`
	$(CC) $(CFLAGS) -c -o $@ $<

# generic link a c++ executable rule
bin/% : tmp/main_%.cpp.o $(CXX_OBJ_PARTS) $(C_OBJ_PARTS) 
	mkdir -p `dirname $@`
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

# generic link a c executable rule  (skip c++ components)
bin/% : tmp/main_%.c.o $(C_OBJ_PARTS) 
	mkdir -p `dirname $@`
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

# generic link a test executable rule
bin/test_% : tmp/test_%.cpp.o $(CXX_OBJ_PARTS) $(C_OBJ_PARTS)
	mkdir -p `dirname $@`
	$(CXX) $(CXXFLAGS) $(GOOGLE_TEST_FLAGS) -o $@ $^ $(LDFLAGS) $(GOOGLE_TEST_LIBS)

# generic link a test executable rule
bin/test_% : tmp/test_%.c.o $(C_OBJ_PARTS)
	mkdir -p `dirname $@`
	$(CXX) $(CXXFLAGS) $(GOOGLE_TEST_FLAGS) -o $@ $^ $(LDFLAGS) $(GOOGLE_TEST_LIBS)
