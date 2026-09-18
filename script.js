
        let ytPlayer;
        function onYouTubeIframeAPIReady() {
            ytPlayer = new YT.Player('yt-player', {
                height: '1',
                width: '1',
                videoId: 'd6KTJpMLe1g',
                playerVars: {
                    'playsinline': 1,
                    'loop': 1,
                    'playlist': 'd6KTJpMLe1g', // Required for loop to work
                    'origin': window.location.origin
                }
            });
        }
    