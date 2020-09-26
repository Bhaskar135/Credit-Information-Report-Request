
$(function(){
    $('.dropdown-item').on('focus',function(){
        $(this).css('background-color','rgb(219, 219, 219)');
        $(this).css('color','black');
    });
    $('.name-checking').on('blur',function(){
        var text=$('.name-checking').val();
        for(var i=0;i<text.length;i++){
            if(text[i]=='&' || text[i]=='@' || text[i]=='#' || text[i]=='$' || text[i]=='%' || text[i]=='^' || text[i]=='*' || text[i]=='!' || text[i]=='~'){
                $('.name-checking').val("");
                $('.con-req-name-fdbck').text("You entered a invalid character.");
                break;
            }
        }
    });
    $('.address-checking').on('focus',function(){
        $('.con-req-address-fdbck').text("");
    });
    $('.address-checking').on('blur',function(){
        var text=$('.address-checking').val();
        for(var i=0;i<text.length;i++){
            if(text[i]=='&' || text[i]=='@' || text[i]=='#' || text[i]=='$' || text[i]=='%' || text[i]=='^' || text[i]=='*' || text[i]=='!' || text[i]=='~'){
                $('.address-checking').val("");
                $('.con-req-address-fdbck').text("You entered a invalid character.");
                break;
            }
        }
    });
    $('.email-valid').on('focus',function(){
        $('.email-valid-fdbck').text("");
    });
    $('.email-valid').on('blur',function(){
        if($('.email-valid').val()==0){
            $('.email-valid-fdbck').text("");
        }else if(emailValidation()){
            $('.email-valid-fdbck').text("");
        }else{
            $('.email-valid-fdbck').text("Enter a valid email.");
            $('.email-valid').val("");
        }
    });
    function emailValidation(){
        if(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test($('.email-valid').val())){
            return true;
        }else{
            return false;
        }
    }
    $('#reg-username').on('focus',function(){
        $('#reg-username-feedback').text("");
    });
    $('#reg-username').on('blur',function(){
        if($('#reg-username').val().length<5){
            $('#reg-username-feedback').text("Username is too short.");
            $('#reg-username').val("");
        }else{
            $('#reg-username-feedback').text("");
        }
    });
    $('.password').on('focus',function(){
        $('.password-feedback').text("");
    });
    $('.password').on('blur',function(){
        if($('.password').val().length>0 && $('.password').val().length<5){
            $('.password-feedback').text("Password is too short.");
            $('.password').val("");
        }else{
            $('.password-feedback').text("");
        } 
    });
    $('.password2').on('focus',function(){
        $('.password2-feedback').text("");
    });
    $('.password2').on('blur',function(){
        if($('.password2').val()!=$('.password').val()){
            $('.password2-feedback').text("Password is not matching.");
            $('.password2').val("");
        }else{
            $('.password2-feedback').text("");
        } 
    });
    $('.con-req-pan').on('focus',function(){
        $('.con-req-pan-fdbck').text("");
    });
    $('.con-req-pan').on('blur',function(){
        if($('.con-req-pan').val()==0){
            $('.con-req-pan-fdbck').text("");
        }else if(panValidation()){
            $('.con-req-pan-fdbck').text("");
        }else{
            $('.con-req-pan-fdbck').text("Enter a valid PAN No.");
            $('.con-req-pan').val("");
        }
    });
    function panValidation(){
        if(/[A-Z]{5}[0-9]{4}[A-Z]{1}$/.test($('.con-req-pan').val())){
            return true;
        }else{
            return false;
        }
    }
    $('.con-req-aadhaar').on('blur',function(){
        if($('.con-req-aadhaar').val().length==0){
            $('.con-req-aadhaar-fdbck').text("");
        }else if($('.con-req-aadhaar').val().length<12||$('.con-req-aadhaar').val().length>12){
            $('.con-req-aadhaar-fdbck').text("Invalid Aadhaar No.");
            $('.con-req-aadhaar').val("");
        }else{
            $('.con-req-aadhaar-fdbck').text("");
        } 
    });
    $('.con-req-aadhaar').on('focus',function(){
        $('.con-req-aadhaar-fdbck').text("");
    });
    $('.con-req-voter').on('blur',function(){
        if($('.con-req-voter').val().length==0){
            $('.con-req-voter-fdbck').text("");
        }else if($('.con-req-voter').val().length<10||$('.con-req-voter').val().length>10){
            $('.con-req-voter-fdbck').text("Invalid Voter ID.");
            $('.con-req-voter').val("");
        }else{
            $('.con-req-voter-fdbck').text("");
        } 
    });
    $('.con-req-voter').on('focus',function(){
        $('.con-req-voter-fdbck').text("");
    });
    $('.con-req-pin').on('focus',function(){
        $('.con-req-pin-fdbck').text("");
    });
    $('.con-req-pin').on('blur',function(){
        if($('.con-req-pin').val().length==0){
            $('.con-req-pin-fdbck').text("");
        }else if(pinValidation()){
            $('.con-req-pin-fdbck').text("");
        }else{
            $('.con-req-pin-fdbck').text("Enter a valid Pin No.");
            $('.con-req-pin').val("");
        }
    });
    function pinValidation(){
        if(/^[1-9]{1}[0-9]{5}$/.test($('.con-req-pin').val())){
            return true;
        }else{
            return false;
        }
    }
    // $('.logout').on('click',function(){
    //     alert("Do you want to logout?");
    // });
    var flag=0;
    $('.deleteUser').on('click',function(){
        $('.userCheckbox').each(function(){
            if($(this).prop("checked")){
                flag=1;
                console.log(flag);
                return false;
            }else{
                flag=0;
                console.log(flag);
            }
        });
        if(flag==0){
            $('.deleteUserText1').hide();
            $('.modalYes').hide();
            $('.modalNo').hide();
            $('.deleteUserText2').show();
            $('.modalOkay').show();
        }else{
            $('.deleteUserText2').hide();
            $('.modalOkay').hide();
            $('.deleteUserText1').show();
            $('.modalYes').show();
            $('.modalNo').show();
            
        }
    });
});






