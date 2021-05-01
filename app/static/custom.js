$(document).ready(function() {
    $('.ui.dropdown').dropdown();
    $('.env.ui.dropdown').dropdown();

    $('.config.item').click(function() {
        var name = $(this).html();
        let env = document.getElementsByClassName('env item selected')[0] ? document.getElementsByClassName('env item selected')[0].innerText: 'dev';
        load_env_config(env);
    });

    $('.env.item').click(function() {
        $('#env-header').hide();
        $('#domain').hide();
        $('#domain_cards').fadeIn();
        $('#main_config_name').hide();
        $('#main_config_content').hide();
    });

    $('#domains').click(function() {
        let env = document.getElementsByClassName('env item selected')[0] ? document.getElementsByClassName('env item selected')[0].innerText: 'dev';
//        console.log(0, env);
        load_env_domains(env);
    });
});

function load_domains() {
    $.when(fetch_html('api/domains')).then(function() {
        $('#domain').hide();
        $('#domain_cards').fadeIn();
    });
}

function load_env_domains(env) {
    $.when(fetch_env_html('api/env/domains/' + env)).then(function() {
        $('#domain').hide();
        $('#domain_cards').fadeIn();
    });
}

function add_domain() {
    let name = $('#add_domain').val();
    $('#add_domain').val('');

    $.ajax({
        type: 'POST',
        url: '/api/domain/' + name,
        statusCode: {
            201: function() { fetch_domain(name) }
        }
    });
}

function add_env_domain() {
    let name = $('#add_env_domain').val();
    let env = document.getElementsByClassName('env item selected')[0] ? document.getElementsByClassName('env item selected')[0].innerText: 'dev';
    let env_domain = env + '-' + name;
    console.log("add env domain:", env_domain);

    $('#add_env_domain').val('');

    $.ajax({
        type: 'POST',
        url: '/api/env/domain/' + env_domain,
        statusCode: {
            201: function() { fetch_env_domain(env_domain) }
        }
    });
}

function reload_nginx() {
    $.ajax({
        type: 'POST',
        url: '/api/ng-reload'
//        statusCode: {
//            201: "reload"
//        }
    });
}

function enable_domain(name, enable) {
    $.ajax({
        type: 'POST',
        url: '/api/domain/' + name + '/enable',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify({
            enable: enable
        }),
        statusCode: {
            200: function() { fetch_domain(name); }
        }
    });

}

function update_domain(name) {
    var _file = $('#file-content').val();
    $('#dimmer').addClass('active');

    $.ajax({
        type: 'PUT',
        url: '/api/domain/' + name,
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify({
            file: _file
        }),
        statusCode: {
            200: function() { setTimeout(function(){ fetch_domain(name) }, 400) }
        }
    });
}

function fetch_domain(name) {

    fetch('api/domain/' + name)
    .then(function(response) {
        response.text().then(function(text) {
            $('#domain').html(text).fadeIn();
            $('#domain_cards').hide();
        });
    })
    .catch(function(error) {
        console.error(error);
    });

}


function remove_domain(name) {

    $.ajax({
        type: 'DELETE',
        url: '/api/domain/' + name,
        statusCode: {
            200: function() {
                load_domains();
            },
            400: function() {
                alert('Deleting not possible');
            }
        }
    });

}

function fetch_html(url) {
    fetch(url)
    .then(function(response) {
        response.text().then(function(text) {
            $('#content').html(text);
        });
    })
    .catch(function(error) {
        console.error(error);
    });
}


function update_config(name) {
    var _file = $('#file-content').val();
    $('#dimmer').addClass('active');

    $.ajax({
        type: 'POST',
        url: '/api/config/' + name,
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify({
            file: _file
        }),
        statusCode: {
            200: function() {

                setTimeout(function() {
                    $('#dimmer').removeClass('active');
                }, 450);

            }
        }
    });
}


function load_config(name) {
    fetch('api/config/' + name)
    .then(function(response) {
        response.text().then(function(text) {
            $('#content').html(text);
        });
    })
    .catch(function(error) {
        console.error(error);
    });

}


function fetch_env_domain(name) {

    fetch('api/env/domain/' + name)
    .then(function(response) {
        response.text().then(function(text) {
            $('#domain').html(text).fadeIn();
            $('#domain_cards').hide();
        });
    })
    .catch(function(error) {
        console.error(error);
    });

}


function fetch_env_html(url) {
    fetch(url)
    .then(function(response) {
        response.text().then(function(text) {
            $('#content').html(text);
        });
    })
    .catch(function(error) {
        console.error(error);
    });
}

function update_env_domain(name) {
    var _file = $('#file-content').val();
    $('#dimmer').addClass('active');

    let env = document.getElementById('env-header').innerText;
    console.log("update", env);

    let domain_name = env + '-' + name;
    $.ajax({
        type: 'PUT',
        url: '/api/env/domain/' + domain_name,
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify({
            file: _file
        }),
        statusCode: {
            200: function() { setTimeout(function(){ fetch_env_domain(domain_name) }, 400) }
        }
    });
}


function remove_env_domain(name) {
    let env = document.getElementById('env-header').innerText || "dev";
    let domain_name = env + '-' + name;
    console.log("remove", env, domain_name);

    $.ajax({
        type: 'DELETE',
        url: '/api/env/domain/' + domain_name,
        statusCode: {
            200: function() {
                load_env_domains(env);
            },
            400: function() {
                alert('Deleting not possible');
            }
        }
    });

}


function enable_env_domain(name, enable) {
    let env = document.getElementById('env-header').innerText || "dev";
    let domain_name = env + '-' + name;
    console.log("enable", env, domain_name);

    $.ajax({
        type: 'POST',
        url: '/api/env/domain/' + domain_name + '/enable',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify({
            enable: enable
        }),
        statusCode: {
            200: function() { fetch_env_domain(domain_name); }
        }
    });

}


function update_env_config(name) {
    var _file = $('#file-content').val();
    $('#dimmer').addClass('active');

    $.ajax({
        type: 'POST',
        url: '/api/env/config/' + name,
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        data: JSON.stringify({
            file: _file
        }),
        statusCode: {
            200: function() {

                setTimeout(function() {
                    $('#dimmer').removeClass('active');
                }, 450);

            }
        }
    });
}


function load_env_config(env) {
    let url = 'api/env/config/' + env ;
    fetch(url)
    .then(function(response) {
        response.text().then(function(text) {
            $('#content').html(text);
        });
    })
    .catch(function(error) {
        console.error(error);
    });
}