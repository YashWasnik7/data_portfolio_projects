This script demonstrates my python coding skills to scrape data from a webpage. I used Beautiful Soup Library to scrape article titles, respective contents and troubleshooting questions for an AI chat bot.

Sample output:

{
    "titles": {
        "article_title": "Troubleshooting | Core 110f will not boot/respond",
        "subtitle_1": "Problem",
        "subtitle_2": "Causes",
        "subtitle_3": "Troubleshooting Steps"
    },
    "contents": {
        "Problem": "Core 110f is stuck in boot cycle or will not respond. Systems logo may also be showing on display.",
        "Causes": "A corruption of the Q-SYS OS may have occurred.A possible hardware failure has occurred.",
        "Troubleshooting Steps": [
            "Does the Core 110f indicate power?",
            "Did the Core 110f boot and start its design?",
            "Does reconnecting to a known working power source and cable restore power?",
            "Does power cycling the device restore function?",
            "Connect an HDMI monitor to the HDMI output of the Core 110f and power cycle. Does the unit display any information or a boot sequence?"
        ]
    }
}
