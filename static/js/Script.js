$(document).ready(function () {
    $('.close').fadeOut(1);

    $(".close").on("click", function () {
        $("#popup,.close").fadeOut(1);
        $(".d-flex, .flex-row, .flex-column, .shop-item, .flex-colum").css('filter', 'none');
    });
});

$(document).ready(function () {
    $('#notification').on('click', function () {
        $("#popup,.close").hide().fadeIn(1);
        $(".d-flex, .flex-row, .flex-column, .shop-item, .flex-colum").css('filter', 'blur(5px)');
    });
})