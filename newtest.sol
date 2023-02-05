{
    samplestring = "caio come stai"

    startswith = fun (main,prefix) {
        if not istype(main,"string") or not istype(prefix,"string") {
            error("TypeError","Arguments should be strings")
        }
        let mainlist = String.tolist(main)
        let prefixlist = String.tolist(prefix)
        for i=0 to len(prefixlist) {
            if mainlist/i != prefixlist/i {
                return false
            }
        }
        return true
    }

    main = fun() {
        log("Start")
        let time = Time.now()
        log(this.startswith(this.samplestring,"caio"))
        log(Time.delta(time))
        log("End")
    }
}