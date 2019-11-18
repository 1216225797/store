  //----数量加减---
  var num1 = document.getElementById('num1');
 
  //封装函数
  function func(a){
  	
  	 var n1=$('#num1').html();
  
  	switch(a){
  		case 1:
  			var num =parseInt(n1)+1;
  			break;
  		case 2:
	  		if (parseInt(n1)>=2) {
	  			var num =parseInt(n1)-1;
	  			break;
	  			}else{
                    num=1;
                  };
  			      }
	

  	//设置文本
  	$('#num1').html(num);

    //---总价格变化
    n2 = parseFloat(num)*2299.00+'.00';
    $('.xiaoji').html(n2);

    var n11=$('.xiaoji').html();
    var n12=$('.xiaoji2').html();
    var n13=$('.xiaoji3').html();

    var heji = parseInt(n11)+parseInt(n12)+parseInt(n13)+'.00'

    $('.hejia').html(heji);

  }


// ----第二行数量加减----
var num2 = document.getElementById('num2');

//封装函数
function func2(a){
  
   n1=$('#num2').html();

  switch(a){
    case 1:
      var num =parseInt(n1)+1;
      break;
    case 2:
      if (parseInt(n1)>=2) {
        var num =parseInt(n1)-1;
        break;
        }else{
                  num=1;
                };
            }


  //设置文本
  $('#num2').html(num);

  //---总价格变化
  n3 = parseFloat(num)*4080.00+'.00';
  $('.xiaoji2').html(n3);

  var n11=$('.xiaoji').html();
  var n12=$('.xiaoji2').html();
  var n13=$('.xiaoji3').html();

  var heji = parseInt(n11)+parseInt(n12)+parseInt(n13)+'.00'

  $('.hejia').html(heji);
}


// ----第三行数量加减----
var num3 = document.getElementById('num3');

//封装函数
function func3(a){
  
   n1=$('#num3').html();

  switch(a){
    case 1:
      var num =parseInt(n1)+1;
      break;
    case 2:
      if (parseInt(n1)>=2) {
        var num =parseInt(n1)-1;
        break;
        }else{
                  num=1;
                };
            }


  //设置文本
  $('#num3').html(num);

  //---总价格变化
  n4 = parseFloat(num)*189.00+'.00';
  $('.xiaoji3').html(n4);

  var n11=$('.xiaoji').html();
  var n12=$('.xiaoji2').html();
  var n13=$('.xiaoji3').html();

  var heji = parseInt(n11)+parseInt(n12)+parseInt(n13)+'.00'

  $('.hejia').html(heji);
}




//---清空---
  $('.qchu1').click(function(){
    
    //获取单价
    var dk=$('.xiaoji').html();
    //获取总价
    var qk= $('.hejia').html();
    //删除后的价格
    var shaq = parseInt(qk)-parseInt(dk);
    //删除后的总价
    $('.hejia').html(shaq);
    $('.sp1').empty();//清空

    
  })
  $('.qchu2').click(function(){
    //获取单价
    var dk=$('.xiaoji2').html();
    //获取总价
    var qk= $('.hejia').html();
    //删除后的价格
    var shaq = parseInt(qk)-parseInt(dk);
    //删除后的总价
    $('.hejia').html(shaq);
    $('.sp2').empty();//清空
    
  })
  $('.qchu3').click(function(){
    //获取单价
    var dk=$('.xiaoji3').html();
    //获取总价
    var qk= $('.hejia').html();
    //删除后的价格
    var shaq = parseInt(qk)-parseInt(dk);
    //删除后的总价
    $('.hejia').html(shaq);
    $('.sp3').empty();//清空
    
  })

// ----全选-----
var inps = document.getElementsByTagName('input');
 inp=true;
  function funn(n){
    for (var i=0; i<inps.length;i++){
      switch(n){
        case 1:
          inps[i].checked=true;
          break;
        case 2:
          inps[i].checked=false;
          break;
      }
    }
  }


