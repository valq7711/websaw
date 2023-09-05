def register_components(Vue, components_pkg):
    if not components_pkg:
        return
    for module_name in components_pkg:
        if module_name.startsWith('__'):
            continue
        module = components_pkg[module_name]
        c = module.make()
        cid = c.name.split('.')[-1]
        Vue.component(cid, c)
