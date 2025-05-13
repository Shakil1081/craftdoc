$(document).ready(function () {
    // page zoom in and zoom out on click 
    let zoomLevel = 1;
    const zoomInput = $('#zoomInput');
    const zoomInBtn = $('#zoomInBtn');
    const zoomOutBtn = $('#zoomOutBtn');
    const a4panel = $('#a4panel');
    const minZoom = 0.6;
    const maxZoom = 1.4;
    const defaultZoom = .75;
    const zoomStep = 0.1;
    zoomInput.text((defaultZoom * 100) + '%');
    a4panel.css('transform', 'scale(' + defaultZoom + ')');
    zoomInBtn.on('click', function () {
        if (zoomLevel < maxZoom) {
            zoomLevel += zoomStep;
            zoomInput.text(Math.round(zoomLevel * 100) + '%');
            a4panel.css('transform', 'scale(' + zoomLevel + ')');
        }
    });
    zoomOutBtn.on('click', function () {
        if (zoomLevel > minZoom) {
            zoomLevel -= zoomStep;
            zoomInput.text(Math.round(zoomLevel * 100) + '%');
            a4panel.css('transform', 'scale(' + zoomLevel + ')');
        }
    });
    // page zoom in and zoom out on click end


    function setHeaderFooter() {
        const selectedItem = $('.letterhead-item.selected');
        const headerSrc = selectedItem.data('header');
        const footerSrc = selectedItem.data('footer');
        $('#a4panel').css({
            'background-image': 'url(' + headerSrc + '), url(' + footerSrc + ')',
        });
    }
    setHeaderFooter();

    $(document).on('click', '.letterhead-item', function () {
        $('.letterhead-item').removeClass('selected');
        $(this).addClass('selected');
        const imgSrc = $(this).find('.preview-image').attr('src');
        setHeaderFooter();
    });


    //header item click event
    $(document).on('click', '.header-item', function () {
        $('.header-item').removeClass('selected');
        $(this).addClass('selected');
        const headerSrc = $(this).data('header');
        const bgImages = $('#a4panel').css('background-image').split(',');

        // Trim and update only the first one (header)
        if (bgImages.length > 1) {
            bgImages[0] = `url("${headerSrc}")`; // Update header
        } else {
            // Fallback: only one image exists, just add the second manually if needed
            bgImages[0] = `url("${headerSrc}")`;
            bgImages[1] = `url("default-footer.png")`; // change this to your actual footer URL
        }

        $('#a4panel').css('background-image', bgImages.join(','));
    });
    //footer item click event
    $(document).on('click', '.footer-item', function () {
        $('.footer-item').removeClass('selected');
        $(this).addClass('selected');

        const footerSrc = $(this).data('footer');
        const bgImages = $('#a4panel').css('background-image').split(',');

        // Ensure both background layers exist
        if (bgImages.length > 1) {
            bgImages[1] = `url("${footerSrc}")`;
        } else {
            // Fallback: only one image exists, add a header placeholder
            bgImages[0] = bgImages[0] || `url("default-header.png")`;
            bgImages[1] = `url("${footerSrc}")`;
        }

        $('#a4panel').css('background-image', bgImages.join(','));
    });
});