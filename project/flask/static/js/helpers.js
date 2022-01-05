function handleJsonResponse(data) {
  if (!data.success && data.data.redirect) {
    window.location.replace(data.data.redirect)
  }
}

function handleErrorResponse(data) {
  console.error(data);
}

function getCsrfToken() {
  return Cookies.get('csrf_access_token')
}