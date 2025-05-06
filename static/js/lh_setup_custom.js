$(document).ready(function () {
  // page zoom in and zoom out on click
  let zoomLevel = 1;
  const zoomInput = $("#zoomInput");
  const zoomInBtn = $("#zoomInBtn");
  const zoomOutBtn = $("#zoomOutBtn");
  const a4panel = $("#a4panel");
  const minZoom = 0.6;
  const maxZoom = 1.4;
  const defaultZoom = 0.75;
  const zoomStep = 0.1;
  zoomInput.text(defaultZoom * 100 + "%");
  a4panel.css("transform", "scale(" + defaultZoom + ")");
  zoomInBtn.on("click", function () {
    if (zoomLevel < maxZoom) {
      zoomLevel += zoomStep;
      zoomInput.text(Math.round(zoomLevel * 100) + "%");
      a4panel.css("transform", "scale(" + zoomLevel + ")");
    }
  });
  zoomOutBtn.on("click", function () {
    if (zoomLevel > minZoom) {
      zoomLevel -= zoomStep;
      zoomInput.text(Math.round(zoomLevel * 100) + "%");
      a4panel.css("transform", "scale(" + zoomLevel + ")");
    }
  });
  // page zoom in and zoom out on click end

  function setHeaderFooter() {
    const selectedItem = $(".letterhead-item.selected");
    const headerSrc = selectedItem.data("header");
    const footerSrc = selectedItem.data("footer");
    $("#a4panel").css({
      "background-image": "url(" + headerSrc + "), url(" + footerSrc + ")",
    });
  }
  setHeaderFooter();

  $(document).on("click", ".letterhead-item", function () {
    $(".letterhead-item").removeClass("selected");
    $(this).addClass("selected");
    const imgSrc = $(this).find(".preview-image").attr("src");
    setHeaderFooter();
  });

  // //header item click event
  // $(document).on("click", ".header-item", function () {
  //   $(".header-item").removeClass("selected");
  //   $(this).addClass("selected");
  //   const headerSrc = $(this).data("header");
  //   const bgImages = $("#a4panel").css("background-image").split(",");

  //   // Trim and update only the first one (header)
  //   if (bgImages.length > 1) {
  //     bgImages[0] = `url("${headerSrc}")`; // Update header
  //   } else {
  //     // Fallback: only one image exists, just add the second manually if needed
  //     bgImages[0] = `url("${headerSrc}")`;
  //     bgImages[1] = `url("default-footer.png")`; // change this to your actual footer URL
  //   }

  //   $("#a4panel").css("background-image", bgImages.join(","));
  // });
  // //footer item click event
  // $(document).on("click", ".footer-item", function () {
  //   $(".footer-item").removeClass("selected");
  //   $(this).addClass("selected");

  //   const footerSrc = $(this).data("footer");
  //   const bgImages = $("#a4panel").css("background-image").split(",");

  //   // Ensure both background layers exist
  //   if (bgImages.length > 1) {
  //     bgImages[1] = `url("${footerSrc}")`;
  //   } else {
  //     // Fallback: only one image exists, add a header placeholder
  //     bgImages[0] = bgImages[0] || `url("default-header.png")`;
  //     bgImages[1] = `url("${footerSrc}")`;
  //   }

  //   $("#a4panel").css("background-image", bgImages.join(","));
  // });

  $("#emailInput").on("input", function () {
    const email = $(this).val();
    const formattedEmail = email.replace(/\n/g, "<br>"); // Convert newlines to <br>
    $("#emailShow").html(formattedEmail);
  });
  $("#phoneInput").on("input", function () {
    const phone = $(this).val();
    const formattedPhone = phone.replace(/\n/g, "<br>"); // Convert newlines to <br>
    $("#phoneShow").html(formattedPhone);
  });
  $("#locationInput").on("input", function () {
    const location = $(this).val();
    const formattedLocation = location.replace(/\n/g, "<br>"); // Convert newlines to <br>
    $("#locationShow").html(formattedLocation);
  });

  $("#logoInput").on("change", function () {
    const file = this.files[0]; // Get the selected file

    if (file) {
      const reader = new FileReader();

      reader.onload = function (e) {
        // Update the source of both the preview and the logo show image
        $("#logoPreview").attr("src", e.target.result);
        $("#logoShow").attr("src", e.target.result); // Update the #logoShow image
      };

      reader.readAsDataURL(file); // Read the file as a Data URL
    }
  });

  //position start
  $("#phoneLeft, #phoneRight, #phoneTop, #phoneBottom").on(
    "input",
    function () {
      const left = parseInt($("#phoneLeft").val(), 10) || 0;
      const right = parseInt($("#phoneRight").val(), 10) || 0;
      const top = parseInt($("#phoneTop").val(), 10) || 0;
      const bottom = parseInt($("#phoneBottom").val(), 10) || 0;

      // Update CSS based on left and right
      if (this.id === "phoneLeft") {
        $("#phoneRight").val(""); // Clear the right input when left is changed
        $("#phoneShow").css({ left: `${left}px`, right: "unset" }); // Set left, reset right
      } else if (this.id === "phoneRight") {
        $("#phoneLeft").val(""); // Clear the left input when right is changed
        $("#phoneShow").css({ right: `${right}px`, left: "unset" }); // Set right, reset left
      }

      // Update CSS based on top and bottom
      if (this.id === "phoneTop") {
        $("#phoneBottom").val(""); // Clear the bottom input when top is changed
        $("#phoneShow").css({ top: `${top}px`, bottom: "unset" }); // Set top, reset bottom
      } else if (this.id === "phoneBottom") {
        $("#phoneTop").val(""); // Clear the top input when bottom is changed
        $("#phoneShow").css({ bottom: `${bottom}px`, top: "unset" }); // Set bottom, reset top
      }
    }
  );

  $("#emailLeft, #emailRight, #emailTop, #emailBottom").on(
    "input",
    function () {
      const left = parseInt($("#emailLeft").val(), 10) || 0;
      const right = parseInt($("#emailRight").val(), 10) || 0;
      const top = parseInt($("#emailTop").val(), 10) || 0;
      const bottom = parseInt($("#emailBottom").val(), 10) || 0;

      if (this.id === "emailLeft") {
        $("#emailRight").val("");
        $("#emailShow").css({ left: `${left}px`, right: "unset" });
      } else if (this.id === "emailRight") {
        $("#emailLeft").val("");
        $("#emailShow").css({ right: `${right}px`, left: "unset" });
      }

      if (this.id === "emailTop") {
        $("#emailBottom").val("");
        $("#emailShow").css({ top: `${top}px`, bottom: "unset" });
      } else if (this.id === "emailBottom") {
        $("#emailTop").val("");
        $("#emailShow").css({ bottom: `${bottom}px`, top: "unset" });
      }
    }
  );

  $("#locationLeft, #locationRight, #locationTop, #locationBottom").on(
    "input",
    function () {
      const left = parseInt($("#locationLeft").val(), 10) || 0;
      const right = parseInt($("#locationRight").val(), 10) || 0;
      const top = parseInt($("#locationTop").val(), 10) || 0;
      const bottom = parseInt($("#locationBottom").val(), 10) || 0;

      if (this.id === "locationLeft") {
        $("#locationRight").val("");
        $("#locationShow").css({ left: `${left}px`, right: "unset" });
      } else if (this.id === "locationRight") {
        $("#locationLeft").val("");
        $("#locationShow").css({ right: `${right}px`, left: "unset" });
      }

      if (this.id === "locationTop") {
        $("#locationBottom").val("");
        $("#locationShow").css({ top: `${top}px`, bottom: "unset" });
      } else if (this.id === "locationBottom") {
        $("#locationTop").val("");
        $("#locationShow").css({ bottom: `${bottom}px`, top: "unset" });
      }
    }
  );
  //position end

  // align start
  $("#emailLeftAlign, #emailCenterAlign, #emailRightAlign").on(
    "click",
    function () {
      $(".align-icon").removeClass("selected");
      $(this).addClass("selected");
      if (this.id === "emailLeftAlign") {
        $("#emailShow").css("text-align", "left");
      } else if (this.id === "emailCenterAlign") {
        $("#emailShow").css("text-align", "center");
      } else if (this.id === "emailRightAlign") {
        $("#emailShow").css("text-align", "right");
      }
    }
  );

  $("#phoneLeftAlign, #phoneCenterAlign, #phoneRightAlign").on(
    "click",
    function () {
      $("#phoneLeftAlign, #phoneCenterAlign, #phoneRightAlign").removeClass(
        "selected"
      );
      $(this).addClass("selected");
      if (this.id === "phoneLeftAlign") {
        $("#phoneShow").css("text-align", "left");
      } else if (this.id === "phoneCenterAlign") {
        $("#phoneShow").css("text-align", "center");
      } else if (this.id === "phoneRightAlign") {
        $("#phoneShow").css("text-align", "right");
      }
    }
  );

  $("#locationLeftAlign, #locationCenterAlign, #locationRightAlign").on(
    "click",
    function () {
      $(
        "#locationLeftAlign, #locationCenterAlign, #locationRightAlign"
      ).removeClass("selected");
      $(this).addClass("selected");
      if (this.id === "locationLeftAlign") {
        $("#locationShow").css("text-align", "left");
      } else if (this.id === "locationCenterAlign") {
        $("#locationShow").css("text-align", "center");
      } else if (this.id === "locationRightAlign") {
        $("#locationShow").css("text-align", "right");
      }
    }
  );
  // align end

  //bold start
  $("#phoneBoldInput").on("click", function () {
    const isBold = $("#phoneShow").css("font-weight") === "700";
    const newFontWeight = isBold ? "500" : "700";
    $("#phoneShow").css("font-weight", newFontWeight);
    $(this).toggleClass("selected", !isBold);
  });

  $("#phoneItalicInput").on("click", function () {
    const isItalic = $("#phoneShow").css("font-style") === "italic";
    const newFontStyle = isItalic ? "normal" : "italic";
    $("#phoneShow").css("font-style", newFontStyle);
    $(this).toggleClass("selected", !isItalic);
  });

  $("#phoneFontFamily").on("change", function () {
    const fontFamily = $(this).val();
    $("#phoneShow").css("font-family", fontFamily || "");
  });

  $("#phoneFontSize").on("input", function () {
    const fontSize = $(this).val();
    if (fontSize) {
      $("#phoneShow").css("font-size", fontSize + "px");
    }
  });

  $("#emailBoldInput").on("click", function () {
    const isBold = $("#emailShow").css("font-weight") === "700";
    const newFontWeight = isBold ? "500" : "700";
    $("#emailShow").css("font-weight", newFontWeight);
    $(this).toggleClass("selected", !isBold);
  });

  $("#emailItalicInput").on("click", function () {
    const isItalic = $("#emailShow").css("font-style") === "italic";
    const newFontStyle = isItalic ? "normal" : "italic";
    $("#emailShow").css("font-style", newFontStyle);
    $(this).toggleClass("selected", !isItalic);
  });

  $("#emailFontFamily").on("change", function () {
    const fontFamily = $(this).val();
    $("#emailShow").css("font-family", fontFamily || "");
  });

  $("#emailFontSize").on("input", function () {
    const fontSize = $(this).val();
    if (fontSize) {
      $("#emailShow").css("font-size", fontSize + "px");
    }
  });

  $("#locationBoldInput").on("click", function () {
    const isBold = $("#locationShow").css("font-weight") === "700";
    const newFontWeight = isBold ? "500" : "700";
    $("#locationShow").css("font-weight", newFontWeight);
    $(this).toggleClass("selected", !isBold);
  });

  $("#locationItalicInput").on("click", function () {
    const isItalic = $("#locationShow").css("font-style") === "italic";
    const newFontStyle = isItalic ? "normal" : "italic";
    $("#locationShow").css("font-style", newFontStyle);
    $(this).toggleClass("selected", !isItalic);
  });

  $("#locationFontFamily").on("change", function () {
    const fontFamily = $(this).val();
    $("#locationShow").css("font-family", fontFamily || "");
  });

  $("#locationFontSize").on("input", function () {
    const fontSize = $(this).val();
    if (fontSize) {
      $("#locationShow").css("font-size", fontSize + "px");
    }
  });
  //bold end

  //color start
  $("#phoneColorInput").on("input", function () {
    const color = $(this).val();
    $("#phoneShow").css("color", color);
  });

  $("#emailColorInput").on("input", function () {
    const color = $(this).val();
    $("#emailShow").css("color", color);
  });

  $("#locationColorInput").on("input", function () {
    const color = $(this).val();
    $("#locationShow").css("color", color);
  });
  //color end

  //logo action
  // Position controls for logo
  $("#logoLeft, #logoRight, #logoTop, #logoBottom").on("input", function () {
    const left = parseInt($("#logoLeft").val(), 10) || 0;
    const right = parseInt($("#logoRight").val(), 10) || 0;
    const top = parseInt($("#logoTop").val(), 10) || 0;
    const bottom = parseInt($("#logoBottom").val(), 10) || 0;

    if (this.id === "logoLeft") {
      $("#logoRight").val("");
      $("#logoShow").css({ left: `${left}px`, right: "" });
    } else if (this.id === "logoRight") {
      $("#logoLeft").val("");
      $("#logoShow").css({ right: `${right}px`, left: "" });
    }

    if (this.id === "logoTop") {
      $("#logoBottom").val("");
      $("#logoShow").css({ top: `${top}px`, bottom: "" });
    } else if (this.id === "logoBottom") {
      $("#logoTop").val("");
      $("#logoShow").css({ bottom: `${bottom}px`, top: "" });
    }
  });

  // Size controls for logo
  $("#logoWidthInput").on("input", function () {
    const width = $(this).val();
    $("#logoHeightInput").val("");
    if (width) {
      $("#logoShow").css({
        width: width + "px",
        height: "auto",
      });
    }
  });

  $("#logoHeightInput").on("input", function () {
    const height = $(this).val();
    $("#logoWidthInput").val("");
    if (height) {
      $("#logoShow").css({
        height: height + "px",
        width: "auto",
      });
    }
  });
});
