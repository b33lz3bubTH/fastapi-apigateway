def exclusion_check(exclude_list, URL, method):
    for (route_method, route_def) in exclude_list:
        if(route_method != method): continue
        route_frags = route_def.split("/")
        if(len(route_frags) != len(URL)): continue
        index, flag = 0 , True
        while index < len(route_frags):
            if route_frags[index].startswith(':'):
                index += 1
                continue
            if route_frags[index] != URL[index]:
                flag = False
                break
            index += 1
        if flag: return True
    return False