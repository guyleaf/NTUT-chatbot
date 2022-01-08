$(function () {
  const Helpers = (function () {
    let Helpers = function () { }
    Helpers.prototype.handleJsonResponse = (data) => {
      if (data.data && data.data.redirect) {
        window.location.replace(data.data.redirect)
      }
    }

    Helpers.prototype.handleErrorResponse = (data) => {
      console.error(data);
    }

    Helpers.prototype.ajax = (method, url, data, dataType = "json") => {
      return $.ajax({
        type: method,
        url: url,
        headers: {
          'X-CSRF-TOKEN': getCsrfToken()
        },
        data: data,
        contentType: "application/json; charset=UTF-8",
        dataType: dataType
      });
    }

    Helpers.prototype.unbindEvent = (target, eventName) => {
      $(target).unbind(eventName);
    }

    function getCsrfToken() {
      return Cookies.get('csrf_access_token');
    }
    return Helpers;
  })();

  window.helpers = new Helpers();
})

