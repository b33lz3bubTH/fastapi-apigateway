def exclusion_check(exclude_list, URL, method):
    for (route_method, route_def) in exclude_list:
        if(route_method != method): continue
        route_frags = route_def.split("/")
        if(len(route_frags) != len(URL)): continue
        i = 0
        flag = True
        for route_frag in route_frags:
            if route_frag.startswith(':'):
                i += 1
                continue
            if route_frag != URL[i]:
                flag = False
                break
            i += 1
        if flag:
            return True
    return False