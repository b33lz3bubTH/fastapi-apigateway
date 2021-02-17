def exclusion_check(exclude_list, URL):
   for route_def in exclude_list:
        route_frags = route_def.split("/")
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
    finally:
    	return False



print(exclusion_check(["admin/:id/posts/:pid"], "admin/100/posts/200".split("/")))
