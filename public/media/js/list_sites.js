$(document).ready(function(){
    $('#list_selector a').live('click', function(e){
        e.preventDefault();
        clicked = $(this).attr('id');
        clicked = clicked.replace('show_site_', '');
       // $('.site_list ul').hide();
        $('.site_list ul').each(function(sites){
            if ($(this).attr('id') != 'site_list_'+clicked){
                console.log($(this).attr('id'))
                $(this).hide();
            }         
        });
        $('#site_list_'+clicked).show();        
    });
    $('.site_list ul:not(:first)').hide();
});