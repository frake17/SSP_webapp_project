$(document).ready(function () {

    $('#filters :checkbox').click(function () {
        if ($('input:checkbox:checked').length) {
            $('.shop-item').hide();
            $('input:checkbox:checked').each(function () {
                $('.shop-item[data-' + $(this).prop('name') + '*="' + $(this).val() + '"]').show();
            });
        } else {
            $(".shop-item").show();
        }
    });

});