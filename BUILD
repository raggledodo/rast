licenses(["notice"])

package(
    default_visibility = [ "//visibility:public" ],
)

# all source files
filegroup(
    name = "srcs",
    srcs = [
        ":rast_py",
        ":test_py",
        "//example:srcs",
        "BUILD",
    ],
)

# main source files
filegroup(
    name = "rast_py",
    srcs = [
        "rast/ast.py",
        "rast/gen.py",
        "rast/last.py",
        "rast/parse.py",
        "rast/plugin.py",
    ],
)

# test source files
filegroup(
    name = "test_py",
    srcs = [
        "rast/test_ast.py",
        "rast/test_gen.py",
        "rast/test_parse.py",
        "rast/test.py",
    ],
)

# ===== LIBRARY =====
py_library(
    name = "rast",
    srcs = [ ":rast_py" ],
)

# ===== TEST =====
py_test(
    name = "test",
    srcs = [ ":test_py" ],
    deps = [ ":rast" ],
    data = [ "//example:cfgs" ],
)
