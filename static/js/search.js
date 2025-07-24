$(document).ready(function () {
  let debounceTimer;

  $("#search").autocomplete({
    source: "/autocomplete",
    minLength: 2
  });

  $('#search').on('input', function () {
    clearTimeout(debounceTimer);
    const query = $(this).val();

    debounceTimer = setTimeout(() => {
      $('#loading-spinner').show();

      $.get('/search', { q: query }, function (data) {
        $('#product-list').html(data.html);
        $('#loading-spinner').hide();
      });
    }, 300);
  });
});
