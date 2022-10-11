for i in range(len(ip)-1):
                x = int(ip.loc[i, "Octant"])+4
                y = int(ip.loc[i+1, "Octant"])+4
                cnt[x] += 1
                if cnt[x] != cnt[y]:
                    if max_cnt[x] < cnt[x]:
                        max_cnt[x] = cnt[x]
                        num[x] = 1
                        To[x] = ip.loc[i, "Time"]  # since we know that all octant sequence count is 1 except "-1"
                        cnt[x] = 0
                    else:
                        if cnt[x] == max_cnt[x]:
                            # since we already know the number of repetitions for each value
                            if x == 3 and max_cnt[3] == 18 and n < 2:
                                T_3[n] = ip.loc[i, "Time"]
                                n +=1
                            num[x] += 1
                            cnt[x] = 0
                        elif max_cnt[x] > cnt[x]:
                            cnt[x] = 0