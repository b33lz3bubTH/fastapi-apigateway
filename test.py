def exclusion_check(exclude_list, URL, method):
    for (route_method, route_def) in exclude_list:
        print("ROUTE MOTHODS: ",route_method, method, (route_method != method) )
        if(route_method != method): continue
        route_frags = route_def.split("/")
        print("FRAG LEN: ", len(route_frags), len(URL))
        if(len(route_frags) != len(URL)): continue

        index, flag = 0 , True
        print("INDEX & FLAG: ",index, flag)
        while index < len(route_frags):
            print("IN LOOP")
            if route_frags[index].startswith(':'):
                print("URL STARTS WITH: ", route_frags[index].startswith(':'))
                index += 1
                continue
            if route_frags[index] != URL[index]:
                print("URL INDEX: ",route_frags[index],  URL[index])
                flag = False
                break
            index += 1

        if flag: return True
    
    return False

res = exclusion_check([("GET", "admin/:user_id"),
			("POST", "admin/:user_id/posts")], "user/2002".split("/"), "POST")

print("THIS ROUTE IS PRESENT: ", res)

