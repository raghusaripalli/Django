$(document).ready(function(){
    var helperpath = $('meta[name=staticpath]').attr("content");
    $('.collapsible').collapsible();
    $('.tooltipped').tooltip({delay: 50});
    $('select').material_select();
    var updateid = 1;
    var updateList = 0;
    var parentToTrigger = 0;
    var parentlist = 0;
    var listid = 0;
    $(document).ready(function() {
        $('input#input_text, textarea#textarea1').characterCounter();
      });
    $('.modal').modal({
          dismissible: true, // Modal can be dismissed by clicking outside of the modal
          opacity: .5, // Opacity of modal background
          inDuration: 300, // Transition in duration
          outDuration: 200, // Transition out duration
          startingTop: '4%', // Starting top style attribute
          endingTop: '10%', // Ending top style attribute
          ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
            console.log(modal, trigger);
            var s = trigger.attr("class").split(" ")[0];
            if (s=="Updatelist")
            {
                var mylist = trigger.parents().eq(1);
                updateList = mylist;
                var id = mylist.attr("id");
                updateid = id;
            }
            else if (s=="CreateItemBtn")
            {
                var mylist = trigger.parents().eq(2);
                updateList = mylist;
                var id = mylist.attr("id");
                updateid = id;
                console.log(id);
                console.log($(updateList));
                parentToTrigger = trigger.parents().eq(1);
                console.log($(parentToTrigger));
            }
            else if(s=="UpdateItem"){
                var mylist = trigger.parents().eq(1);
                updateList = mylist;
                var id = mylist.attr("id");
                updateid = id;
                console.log(id);
                console.log($(updateList));
                parentlist = mylist.parents().eq(1);
                listid = parentlist.attr("id");
                console.log($(parentlist));
                console.log(listid);
            }
          },
          complete: function(){

          }
        }
    );

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $.get("restlist/", function(data, status){
        $.get(helperpath+'showList.html', function(myhtml){
            $.template('mytodolist', myhtml);
            $.tmpl( "mytodolist", data ).appendTo( "#mylist");;
        });
    });

    $("#search").keyup(function(){
        var b = $(this).val();
        var arr = $("#mylist").find("li");
        for (i=0;i<arr.length;i++){
            var n = $(arr[i]).find("h5")[0];
            console.log(n);
            if ($(n).text().includes(b))
                $(arr[i]).show();
            else
                $(arr[i]).hide();
        }
    });

    $("body").on('click','.collapsible-header', function(){
       var p = $(this).parent();
        var id = $(p).attr("id");
        var c = $(p).attr("class");
        if (c.includes("active")){
            var k = $(p).children(".collapsible-body");
            if ($(k).html()==""){
                $(k).append('<div class="center"><a class="CreateItemBtn modal-trigger waves-effect waves-light btn-flat waves-teal" href="#modal3">Create New Item</a></div><br>');
                $.get("restlist/"+id+"/restitem/", function(data, status){
                     $.get(helperpath+'showItems.html', function(myhtml){
                        $.template('mytodolist', myhtml);
                        $.tmpl( "mytodolist", data ).appendTo( k );
                    });
                });
            }
        }
    });

    $( "#form1" ).submit(function( event ) {
      event.preventDefault();
      var formdata = $( this ).serializeArray();
      data = {}
      for (i=0;i<formdata.length;i++){
        data[formdata[i].name] = formdata[i].value;
      }
        var posting = $.post( "restlist/", data, function( data ) {
            $.get(helperpath+'showList.html', function(myhtml){
                $.template('mytodolist', myhtml);
                $.tmpl( "mytodolist", data ).appendTo( "#mylist" );
            });
        }, "json");
    });

    $( "#form2" ).submit(function( event ) {
          var id = updateid;
          event.preventDefault();
          var formdata = $( this ).serializeArray();
          data = {};
          for (i=0;i<formdata.length;i++){
            data[formdata[i].name] = formdata[i].value;
          }
          $.ajax({
            url: 'restlist/'+id+'/',
            type: 'PUT',
            data: data,
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
            },
            success: function(result) {
                var n = updateList.find("h5")[0];
                n["outerHTML"] =  "<h5>"+data['name']+"</h5>";

            }
          });
        });

    $( "#form3" ).submit(function( event ) {
      event.preventDefault();
      id = updateid;
      var formdata = $( this ).serializeArray();
      data = {}
      for (i=0;i<formdata.length;i++){
        data[formdata[i].name] = formdata[i].value;
      }
      if (data['completed']=="on") data['completed']= true;
      else data['completed'] = false;
      console.log(data);
        var posting = $.post( "restlist/"+id+"/restitem/", data, function( data ) {
            $.get(helperpath+'showItems.html', function(myhtml){
                $.template('mytodolist', myhtml);
                $.tmpl( "mytodolist", data ).appendTo( parentToTrigger );
            });
        }, "json");
    });

    $( "#form4" ).submit(function( event ) {
          var id = updateid;
          event.preventDefault();
          var formdata = $( this ).serializeArray();
          data = {};
          for (i=0;i<formdata.length;i++){
            data[formdata[i].name] = formdata[i].value;
          }
          $.ajax({
            url: 'restlist/'+listid+'/restitem/'+id+'/',
            type: 'PUT',
            data: data,
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
            },
            success: function(result) {
                var n = $(updateList).find("div");
                $(n[0]).text(data['description']);
                $(n[1]).text(data['due_by']);
                if (data['completed']=="on")
                    $(n[2]).text("true");
                else
                    $(n[2]).text("false");
            }
          });
        });

    $("body").on('click','.Deletelist',function(){
        var mylist = $(this).parents().eq(1);
        console.log(mylist);
        var id = mylist.attr("id");
        console.log(id);
        $.ajax({
            url: 'restlist/'+id+'/',
            type: 'DELETE',
            beforeSend: function(xhr) {
            if (confirm("Do you really want to delete ?"))
                xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
                else return;
            },
            success: function(result) {
                mylist.fadeIn("fast", function() {
                  $(this).delay(500).fadeOut("slow");
                });
            }
        });
    });

    $("body").on('click','.Deleteitem',function(){
        var mylist = $(this).parents().eq(1);
        updateList = mylist;
        var id = mylist.attr("id");
        updateid = id;
        parentlist = mylist.parents().eq(1);
        listid = parentlist.attr("id");
        $.ajax({
            url: 'restlist/'+listid+'/restitem/'+updateid+'/',
            type: 'DELETE',
            beforeSend: function(xhr) {
                if (confirm("Do you really want to delete ?"))
                xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
                else return;
            },
            success: function(result) {
                mylist.fadeIn(1000).hide();
                mylist.remove();
            }
        });
    });
});
