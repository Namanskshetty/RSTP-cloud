import speedtest as sp

class Upload():
    def check(self):
        try:
            s=sp.Speedtest()
            s.get_servers()
            up=round(s.upload()/(10**6),2)
        except:
            up=0
        return up
def main():
    upl=Upload()
    return upl.check()

if __name__ == "__main__":
    main()
