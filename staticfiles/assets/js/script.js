// function updateDynamicPreview() {
//   $('textarea[id]').each(function () {
//     const textarea = $(this);
//     const textareaId = textarea.attr('id');
//     const textValue = textarea.val().trim();

//     // Map textarea ID to preview class
//     let previewClass = '';
//     if (textareaId.includes('contact')) {
//       previewClass = 'contact-number';
//     } else if (textareaId.includes('email') || textareaId.includes('website')) {
//       previewClass = 'website';
//     } else if (textareaId.includes('address') || textareaId.includes('location')) {
//       previewClass = 'address';
//     } else {
//       return; // Skip if no mapping
//     }

//     // Set default preview content from textarea
//     const inputLines = textValue.split('\n');
//     const newHtml = inputLines.map(line => `<span>${line.trim()}</span>`).join('');
//     $('.' + previewClass).html(newHtml);

//     // Add live update listener
//     textarea.on('input', function () {
//       const updatedLines = textarea.val().split('\n');
//       const updatedHtml = updatedLines.map(line => `<span>${line.trim()}</span>`).join('');
//       $('.' + previewClass).html(updatedHtml);
//     });
//   });
// }

// $(document).ready(function () {
//   updateDynamicPreview();
// });



  $(document).ready(function () {
    $('.font-size-group').each(function () {
      const $input = $(this).find('.font-size-input');
      const $plusBtn = $(this).find('.plus-btn');
      const $minusBtn = $(this).find('.minus-btn');

      $plusBtn.on('click', function () {
        let value = parseInt($input.val()) || 0;
        if (value < 46) $input.val(value + 1);
      });

      $minusBtn.on('click', function () {
        let value = parseInt($input.val()) || 0;
        if (value > 8) $input.val(value - 1);
      });

      $input.on('input', function () {
        let value = parseInt($input.val()) || 0;
        if (value < 8) $input.val(8);
        if (value > 46) $input.val(46);
      });
    });
  });



//   $(document).ready(function () {
//     const $templateItems = $('.template-item');
//     const $headerSection = $('.header-section');
//     const $bodySection = $('.body-section');
//     const $footerSection = $('.footer-section');

//     function setTemplateImages(filename) {
//         const headerPath = `./assets/image/header/${filename}`;
//         const footerPath = `./assets/image/footer/${filename}`;
//         const bodyPath = `./assets/image/body/${filename}`;
    
//         // Set BODY background
//         $bodySection.css({
//             'background-image': `url('${bodyPath}')`,
//             'background-size': 'cover',
//             'background-repeat': 'no-repeat',
//             'background-position': 'center',
//         });
    
//         // HEADER
//         const headerImg = new Image();
//         headerImg.src = headerPath;
//         headerImg.onload = function () {
//             $headerSection.css({
//                 'background-image': `url('${headerPath}')`,
//                 'background-size': '100% auto',
//                 'background-repeat': 'no-repeat',
//                 'background-position': 'top center',
//             });
//         };
    
//         // FOOTER
//         const footerImg = new Image();
//         footerImg.src = footerPath;
//         footerImg.onload = function () {
//             $footerSection.css({
//                 'background-image': `url('${footerPath}')`,
//                 'background-size': '100% auto',
//                 'background-repeat': 'no-repeat',
//                 'background-position': 'bottom center',
//             });
//         };
//     }
  
//     // On load (default)
//     const defaultImage = $templateItems.first().data('image');  // Get the first template item
//     const defaultFilename = defaultImage.split('/').pop(); // Extract the filename (e.g., "1.png")
//     setTemplateImages(defaultFilename); // Set the default images for header, body, and footer
  
//     // On template click
//     $templateItems.on('click', function () {
//         $templateItems.removeClass('selected');  // Remove the "selected" class from all items
//         $(this).addClass('selected');  // Add the "selected" class to the clicked item
    
//         const image = $(this).data('image');  // Get the data-image attribute from the clicked template
//         const filename = image.split('/').pop();  // Extract the filename (e.g., "2.png")
    
//         setTemplateImages(filename);  // Update the header, body, and footer images based on the selected template
//     });
// });



  $(document).ready(function () {
    let zoom = 60;
    const zoomStep = 10;
    const minZoom = 30;
    const maxZoom = 200;

    const $zoomValue = $('#zoomValue');
    const $a4Preview = $('#a4Preview');

    function applyZoom() {
      $a4Preview.css({
        transform: `scale(${zoom / 100})`,
        'transform-origin': 'top center'
      });
      $zoomValue.text(`${zoom}%`);
    }

    $('#zoomIn').on('click', function () {
      if (zoom < maxZoom) {
        zoom += zoomStep;
        applyZoom();
      }
    });

    $('#zoomOut').on('click', function () {
      if (zoom > minZoom) {
        zoom -= zoomStep;
        applyZoom();
      }
    });

    applyZoom(); // Initial zoom
  });


  $(document).ready(function () {
    $('#logoPreview').on('click', function () {
      $('#logoInput').click();
    });

    $('#logoInput').on('change', function (e) {
      const file = e.target.files[0];
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function (e) {
          $('#logoPreview').attr('src', e.target.result);
        };
        reader.readAsDataURL(file);
      }
    });
  });