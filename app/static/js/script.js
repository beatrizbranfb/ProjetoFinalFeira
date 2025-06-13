document.addEventListener('DOMContentLoaded', function() {
    const body = document.body;
    const changeBgButton = document.getElementById('changeBgButton');
    const submitButton = document.getElementById('submitButton');


    function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }


    function darkenColor(hex, percent) {

        hex = hex.replace(/^#/, '');

        let r = parseInt(hex.substring(0, 2), 16);
        let g = parseInt(hex.substring(2, 4), 16);
        let b = parseInt(hex.substring(4, 6), 16);

        r = Math.floor(r * (1 - percent / 100));
        g = Math.floor(g * (1 - percent / 100));
        b = Math.floor(b * (1 - percent / 100));

        r = Math.min(255, Math.max(0, r));
        g = Math.min(255, Math.max(0, g));
        b = Math.min(255, Math.max(0, b));

        const toHex = (c) => ('0' + c.toString(16)).slice(-2);
        return '#' + toHex(r) + toHex(g) + toHex(b);
    }


    function applyBackgroundColor(color) {
        body.style.backgroundColor = color;
        localStorage.setItem('savedBackgroundColor', color);
    }


    const savedColor = localStorage.getItem('savedBackgroundColor');
    if (savedColor) {
        applyBackgroundColor(savedColor);
    } else {

        applyBackgroundColor(getRandomColor());
    }


    if (changeBgButton) {
        changeBgButton.addEventListener('click', function() {
            const newColor = getRandomColor();
            applyBackgroundColor(newColor);
        });
    }

    function addHoverEffect(button) {
        if (button) {
            let originalColor = button.style.backgroundColor || getComputedStyle(button).backgroundColor;

            if (originalColor.startsWith('rgb')) {
                const rgb = originalColor.match(/\d+/g);
                originalColor = '#' + ((1 << 24) + (parseInt(rgb[0]) << 16) + (parseInt(rgb[1]) << 8) + parseInt(rgb[2])).toString(16).slice(1);
            }

            const darkenedColor = darkenColor(originalColor, 15);

            button.addEventListener('mouseenter', function() {
                this.style.backgroundColor = darkenedColor;
            });

            button.addEventListener('mouseleave', function() {
                this.style.backgroundColor = originalColor;
            });
        }
    }
    addHoverEffect(submitButton);
});