$(document).ready(function() {
    loadPartial('sales-charts.html');
});

function loadPartial(page) {
    $.ajax({
        url: 'demo/' + page,
        type: this.method,
        data: $(this).serialize(),
        success: function(result) {
            $('.container-fluid .fade-in').html(result);
        }
    });
}