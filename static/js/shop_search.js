$("#box").on('keyup', function () {
    var matcher = new RegExp($(this).val());
    $('.shop-item').show().not(function () {
        return matcher.test($(this).find('.name').text())
    }).hide();
});