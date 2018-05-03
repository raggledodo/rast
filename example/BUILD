licenses(["notice"])

package(
    default_visibility = [ "//visibility:public" ],
)

# local sources
filegroup(
    name = "srcs",
    srcs = glob([ "*.py" ]) + [
        ":cfgs",
        "BUILD",
    ],
)

# configs
filegroup(
    name = "cfgs",
    srcs = [ "sample.yaml" ]
)

# ===== LIBRARY =====
py_library(
    name = "example_lib",
    srcs = [ "shaped_node.py" ],
    deps = [ "//:rast" ],
    data = [ ":cfgs" ]
)

# ===== EXAMPLE BINARY =====
py_binary(
    name = "example",
    srcs = [ "example.py" ],
    deps = [ ":example_lib" ]
)
