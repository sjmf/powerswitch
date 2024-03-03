/**
 * Power switch control
 * @author Samantha Finnigan, 2021
 */
(function() {
    // Globals
    const power_on_class = "power-on"
    const power_off_class= "power-off"

    const poll_duration = 2500;
    const pulse_duration_ms = 200;

    const form = document.getElementById("control")
    const status = document.getElementById("status")
    const last = document.getElementById("last")
    const body = document.querySelector('body')
    const checkbox = document.querySelector('input[type=checkbox]#read')


    /**
     * Control the timeout loop
     * @return {[type]} [description]
     */
    const timeoutLoop = function() {
        window.clearTimeout(readPin)
        window.setTimeout(readPin, poll_duration)
    }

    /**
     * Handle polling of power status
     * @return {[type]} [description]
     */
    const readPin = function() {
        if (!checkbox.checked) {
            timeoutLoop()
            body.className = "unknown"
            return
        }

        let xhr = new XMLHttpRequest()
        xhr.timeout = poll_duration;

        const handler = function(evt){
            timeoutLoop()

            // Show status
            status.innerHTML = evt.target.response
            if(evt.target.response === "1") {         // Floating
                body.className = power_off_class
            } else if (evt.target.response === "0") { // Pulled down
                body.className = power_on_class
            } else {
                body.className = ""
            }

            // Set time
            last.innerHTML = new Date().toLocaleString()
        }

        xhr.addEventListener("load", handler)
        xhr.addEventListener("error", handler)
        xhr.addEventListener("timeout", () => {
            timeoutLoop()
            body.className = "unknown"
        })

        xhr.open("GET", "/read")
        xhr.send()
    }

    /**
     * Handle form control submission by AJAX (without page reload or navigation)
     * @param  {[type]} e [description]
     * @return {[type]}   [description]
     */
    const formSubmit = function(e) {
        e.preventDefault();
        // console.log(e)
        let xhr = new XMLHttpRequest()

        // Decide which formAction to use (as this is NOT automatic!)
        // If button has a formAction attribute, use that over form.action:
        const parentAction = (new URL(form.action)).pathname
        const buttonAction = (new URL(e.submitter.formAction)).pathname
        const href = (new URL(window.location.href)).pathname

        const url = (buttonAction == href) ? parentAction : buttonAction

        xhr.open("POST", url)
        xhr.setRequestHeader("Content-Type", "application/json")
        //xhr.send("value=" + e.submitter.value + '\n')
        // Support overriding pulse_duration_ms from window object
        xhr.send("duration=" + (window.pulse_duration_ms || pulse_duration_ms))

        console.log("sent XHR Request to " + url)
        e.returnValue = false
        return false
    }

    /**
     * Add handlers and kick off event loop on page load
     */
    document.addEventListener( "DOMContentLoaded", function() {
        form.addEventListener( "submit", formSubmit, false);
        readPin()   // Start poll loop
    });
})();