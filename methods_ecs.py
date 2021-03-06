import os


def generate_dynamic_system_funcs():
    """ Generates the functions needed to convert a scripted system in a
    compile time system. """

    # Compilation performances doesn't change much with 100/500/2000 functions,
    # but 500 functions seems already much after the real needs; in the end
    # this cap is only for scripting systems.
    max_dynamic_systems = 500
    path = "./systems/dynamic_system.gen.h"

    if os.path.exists(path):
        # The file already esists, do not generate it again so the compiler
        # will skip this file if already compiled.
        return

    f = open(path, "w")
    f.write("/* THIS FILE IS GENERATED DO NOT EDIT */\n")
    f.write("#define DYNAMIC_SYSTEMS_MAX " + str(max_dynamic_systems) + "\n")
    f.write("uint32_t registered_dynamic_system_count = 0;\n")
    f.write("godex::DynamicSystemInfo dynamic_info[DYNAMIC_SYSTEMS_MAX];\n")

    # Write functions.
    for i in range(max_dynamic_systems):
        f.write("void dynamic_system_internal_" + str(i) + "(World *p_world) {\n")
        f.write("	godex::DynamicSystemInfo::executor(p_world, dynamic_info[" + str(i) + "]);\n")
        f.write("}\n")

    # Write the array that olds the function pointers.
    f.write("\n")
    f.write("system_execute dynamic_systems_ptr[DYNAMIC_SYSTEMS_MAX] = {\n")
    for i in range(max_dynamic_systems):
        if i > 0:
            f.write(", ")
        f.write("	dynamic_system_internal_" + str(i) + "\n")
    f.write("};\n")

    f.write("\n")
    f.write("system_execute godex::register_dynamic_system(const DynamicSystemInfo &p_info) {\n")
    f.write("	const uint32_t id = registered_dynamic_system_count++;\n")
    f.write("	CRASH_COND_MSG(id >= DYNAMIC_SYSTEMS_MAX, \"You can't register more than \" + itos(DYNAMIC_SYSTEMS_MAX) + \" dynamic systems. Please open an issue so we can increase this limit.\");\n")
    f.write("	dynamic_info[id] = p_info;\n")
    f.write("	return dynamic_systems_ptr[id];\n")
    f.write("}\n")
    f.write("\n")

    f.close()
