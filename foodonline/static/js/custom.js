$(document).ready(function(){

    // add to cart 
    $('.add_to_cart').on('click',function(e){
        e.preventDefault();
        food_id =$(this).attr('data-id');   // capture the data 
        url = $(this).attr('data-url')


        
        // data = {
        //     food_id:food_id,

        // }
        $.ajax({
            type:'GET',
            url:url,
            // data:data,
            success:function(response){
                // console.log(response.cart_counter['cart_count'])    
                if(response.status == 'login_required'){
                    swal(response.message,'','info').then(function(){
                        window.location = '/login';
                    })
                }if(response.status=='Failed'){
                    swal(response.message,'','error')

                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])  // add the class cart_counter html to add it and increase the number of cart in navbar 
                    $('#qty-'+food_id).html(response.qty)  // add the class cart_counter html to add it and increse the cart in vendor_detail.html page 

                }

            }
        })

    })

    // place the cart item quantity on load 

    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        // console.log(qty)

        $('#'+the_id).html(qty)
    })


    // decrease cart 

    $('.decrease_cart').on('click',function(e){
        e.preventDefault();

        food_id =$(this).attr('data-id');   // capture the data 
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');
        


        
        // data = {
        //     food_id:food_id,

        // }

        $.ajax({
            type:'GET',
            url:url,
            // data:data,
            success:function(response){
                // console.log(response.cart_counter['cart_count'])    
                console.log(response)
                if(response.status == 'login_required'){
                    swal(response.message,'','info').then(function(){
                        window.location = '/login';
                    })
                }
                else if(response.status == 'Failed'){
                    swal(response.message,'','error')

                    
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])  // add the class cart_counter html to add it and increase the number of cart in navbar 
                    $('#qty-'+food_id).html(response.qty)  // add the class cart_counter html to add it and increse the cart in vendor_detail.html page 

                    if(window.location.pathname == '/cart/'){
                        removeCartItem(response.qty, cart_id);  // minus button are clicked and when equal to 0 item is remove it 
                        checkEmptyCart();


                    }


                }
                
            }
        })

        function removeCartItem(cartItemQty, cart_id){
            if(cartItemQty <= 0){
                // remove the cart item element 
                document.getElementById("cart-item-"+cart_id).remove()  // use the cart_id and remove it 
            }
        }

    })



});



// delete cart item 

$('.delete_cart').on('click', function(e){
    e.preventDefault();

    cart_id = $(this).attr('data-id');
    url = $(this).attr('data-url');


    $.ajax({
        type: 'GET',
        url: url,
        success: function(response){
            console.log(response)
            if(response.status == 'Failed'){
                swal(response.message, '', 'error')
            }else{
                $('#cart_counter').html(response.cart_counter['cart_count']);
                swal(response.status, response.message, "success")

                

                removeCartItem(0, cart_id);  // remove the caritem using the cart_id 
                checkEmptyCart();

            }
            
        }
    })

    // delete the cart element if the quantity is 0 
    function removeCartItem(cartItemQty, cart_id){
            if(cartItemQty <= 0){
                // remove the cart item element 
                document.getElementById("cart-item-"+cart_id).remove()  // use the cart_id and remove it 
            }

        
        
    }



    // check if the cart is empty 
    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML   // id cart_counter hai html me 
        if(cart_counter == 0){   // when cart_counter is equal to 0 
            document.getElementById("empty-cart").style.display = "block";    // id empty-cart is show when cart_counter is 0 
        }
    }

})



