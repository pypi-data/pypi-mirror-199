def starpix(star_index, updown="up"):
    
    if updown == "up":
        i = 0
        while i <= star_index:
            print("*"*i)
            i += 1
            
    elif updown == "down":
        i = 0
        miner_idx = star_index
        while i <= star_index:
            print("*"*miner_idx)
            miner_idx -= 1
            i += 1