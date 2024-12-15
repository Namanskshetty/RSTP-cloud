import modules.speedtest as sp

speed=sp.main()

if speed<5:
    check=input("The speed is very slow!! ("+str(speed)+") Do you wish to continue Y/N. ")
    if check.lower()!='y':
        prin('Bye')
        exit()
    else:
        print("Continue")
else:
    print("pass")
