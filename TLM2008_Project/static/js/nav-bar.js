        // Get the current page URL
        var currentPage = window.location.pathname;

        // Loop through each navigation link and check if it matches the current page URL
        var navLinks = document.querySelectorAll('.navbar li');
        for (var i = 0; i < navLinks.length; i++) {
            var link = navLinks[i].querySelector('a').getAttribute('href');
            if (link === currentPage) {
                navLinks[i].classList.add('current-page');
            } else {
                navLinks[i].classList.remove('current-page');
            }
        }