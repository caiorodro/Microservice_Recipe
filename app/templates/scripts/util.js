const TituloDaAplicacao = "Recipe and nutrition survey";

let _height;

const divProcessamento = document.createElement('div');

divProcessamento.style.zIndex = '100000';
divProcessamento.style.position = 'fixed';
divProcessamento.style.left = '0px';
divProcessamento.style.top = '0px';
divProcessamento.style.width = '100%';
divProcessamento.style.height = '100%';
divProcessamento.style.backgroundColor = '#FFF';
divProcessamento.style.MozOpacity = '0.4';
divProcessamento.style.opacity = '.40';
divProcessamento.style.filter = 'alpha(opacity=40)';
divProcessamento.style.visibility = 'hidden';

document.body.appendChild(divProcessamento);

this.MensagemDeErro = function (strMensagem) {
    try {
        parent.swal({
            text: strMensagem,
            type: "error",
            showCancelButton: false
        });
    }
    catch (e) {
        swal({
            text: strMensagem,
            type: "error",
            showCancelButton: false
        });
    }
};

this.MensagemDeSucesso = function (strMensagem, fn) {
    try {
        parent.swal({
            text: strMensagem,
            type: "success",
            showCancelButton: false
        }, function () {
            fn();
        });
    }
    catch (e) {
        swal({
            text: strMensagem,
            type: "error",
            showCancelButton: false
        });
    }
};

this.MensagemDeConfirmacao = function (strMensagem, Response) {
    parent.swal({ text: strMensagem, showCancelButton: true }).then(result => {
        if (result) {
            Response();
        }
    }, function (dismiss) {
        if (dismiss === 'cancel') {
            // ignore
        } else {
            throw dismiss;
        }
    });
};

const ptBr = {
    "lengthMenu": "Exibi&ccedil;&atilde;o _MENU_ linhas por p&aacute;gina",
    "zeroRecords": "Nenhum registro encontrado",
    "info": "P&aacute;gina _PAGE_ de _PAGES_&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;_MAX_ registro(s)",
    "infoEmpty": "Sem registros",
    "infoFiltered": "(_TOTAL_ registro(s) filtrado(s) de _MAX_)",
    "thousands": ".",
    "loadingRecords": "Carregando...",
    "processing": "Processando...",
    "search": "Filtro:",
    "select": {
        rows: ""
    },
    "paginate": {
        "first": "Primeira",
        "last": "Ultima",
        "next": "Pr&oacute;xima",
        "previous": "Anterior"
    },
    "aria": {
        "sortAscending": ": Ordenar crescente",
        "sortDescending": ": Ordenar decrescente"
    }
};

const ptBr1 = {
    "lengthMenu": "Exibi&ccedil;&atilde;o _MENU_ linhas por p&aacute;gina",
    "zeroRecords": "Sem registros",
    "info": "",
    "infoEmpty": "",
    "infoFiltered": "(_TOTAL_ registro(s) filtrado(s) de _MAX_)",
    "thousands": ".",
    "loadingRecords": "Carregando...",
    "processing": "Processando...",
    "search": "Filtro:",
    "select": {
        rows: ""
    },
    "paginate": {
        "first": "Primeira",
        "last": "Ultima",
        "next": "Pr&oacute;xima",
        "previous": "Anterior"
    },
    "aria": {
        "sortAscending": ": Ordenar crescente",
        "sortDescending": ": Ordenar decrescente"
    }
};

const getIndexOfColumn = (columnName) => {
    let retorno = -1;

    columns.map(function (item, i) {
        if (item == columnName) {
            retorno = i;
        }
    });

    return retorno;
};

let imgAjaxLoader = document.createElement('img');

imgAjaxLoader.setAttribute('src', 'app/templates/assets/images/preloader3.gif');
imgAjaxLoader.style.position = "fixed";
imgAjaxLoader.style.zIndex = '100001';
imgAjaxLoader.style.left = 50 + "%";
imgAjaxLoader.style.top = 50 + "%";
imgAjaxLoader.style.marginLeft = -32 + "px";
imgAjaxLoader.style.marginTop = -32 + "px";
imgAjaxLoader.style.backgroundColor = "transparent";
imgAjaxLoader.style.visibility = "hidden";

document.body.appendChild(imgAjaxLoader);

const showProcess = (show) => {
    imgAjaxLoader.style.visibility = show ? 'visible' : 'hidden';
    divProcessamento.style.visibility = show ? 'visible' : 'hidden';
}

let processing = false;

const doranAjax = (url, data, success, error, hideProcess) => {
    if (!hideProcess)
        showProcess(true);

    const xerror = error ? error : function (xhr, status, error) {
        showProcess(false);
        processing = false;

        parent.MensagemDeErro(xhr.responseJSON.message);
    };

    processing = true;

    try {
        $.ajax({
            url: url,
            contentType: "application/json",
            datatype: 'json',
            data: JSON.stringify(data),
            type: 'POST',
            success: function (response) {
                showProcess(false);
                processing = false;
                success(response);
            },
            error: xerror
        });
    }
    catch (e) {
        showProcess(false);
    }
};

const aplyOnlyNumbersAndComma = (controls) => {
    controls.map(function (item) {

        $('#' + item).on('keydown', function (e) {
            if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190, 188]) !== -1 ||
                (e.keyCode === 65 && (e.ctrlKey === true || e.metaKey === true)) ||
                (e.keyCode >= 35 && e.keyCode <= 40)) {
                return;
            }

            if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
                e.preventDefault();
            }
        });
    });
};

const aplyOnlyNumbers = (controls) => {
    controls.map(function (item) {

        $('#' + item).on('keydown', function (e) {
            if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190]) !== -1 ||
                (e.keyCode === 65 && (e.ctrlKey === true || e.metaKey === true)) ||
                (e.keyCode >= 35 && e.keyCode <= 40)) {
                return;
            }

            if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
                e.preventDefault();
            }
        });
    });
};

const onlyNumbersFromString = (str1) => {
    const nums = "0123456789";

    const arr1 = str1.split('');
    let retorno = '';

    arr1.map(function (i) {
        if (nums.indexOf(i) > -1)
            retorno += i;
    });

    return parseInt(retorno);
};

const onlyNumbersComaFromString = (str1) => {
    const nums = "0123456789,";

    const arr1 = str1.split('');
    let retorno = '';

    arr1.map(function (i) {
        if (nums.indexOf(i) > -1)
            retorno += i;
    });

    return retorno;
};

const onlyNumbersFromString1 = (str1) => {
    const nums = "0123456789";

    const arr1 = str1.split('');
    let retorno = '';

    arr1.map(function (i) {
        if (nums.indexOf(i) > -1)
            retorno += i;
    });

    return retorno;
};

const EnableDisableElement = (elm, ed) => {

    if (ed)
        $('#' + elm).removeAttr('disabled');
    else if (!ed)
        $('#' + elm).attr('disabled', true);

};
const formatDateToString = (strDt) => {
    const dt = new Date(onlyNumbersFromString(strDt));

    return dt.getFullYear() + '-' +
        ((dt.getMonth() + 1) + '').padLeft('0', 2) + '-' +
        (dt.getDate() + '').padLeft('0', 2);
}

const formatDateToString1 = (strDt) => {
    const x = strDt.split(",");
    const dt = new Date(x[0], x[1], x[2]);

    const dtx = dt.getFullYear() + '-' +
        ((dt.getMonth() + 1) + '').padLeft('0', 2) + '-' +
        (dt.getDate() + '').padLeft('0', 2);

    return dtx;
}

const bsDate = (day, date1) => {
    const dt = date1 ? date1 : new Date();

    const _day = day ? day : dt.getDate();

    return (dt.getFullYear() + '-') +
            ((dt.getMonth() + 1) + '').padLeft('0', 2) + '-' +
            (_day + '').padLeft('0', 2);
};

const bsDateAdd = (days) => {
    const date1 = new Date();
    date1.setDate(date1.getDate() + days);

    return bsDate(0, date1);
};

const bsDateToString = (str1) => {
    return str1.substring(8, 10) + '/' +
        str1.substring(5, 7) + '/' +
        str1.substring(0, 4);
};

const bsDateToString1 = (str1) => {
    return str1.substring(5, 7) + '/' +
        str1.substring(8, 10) + '/' +
        str1.substring(0, 4);
};

const formatDateHourToString = (strDt) => {
    const dt = new Date(onlyNumbersFromString(strDt));

    return (dt.getDate() + '').padLeft('0', 2) + '/' +
        ((dt.getMonth() + 1) + '').padLeft('0', 2) + '/' +
        dt.getFullYear() + ' ' + (dt.getHours() + '').padLeft('0', 2) + ':' +
        (dt.getMinutes() + '').padLeft('0', 2);
}

const getMinutesBetweenDates = (startDate, endDate) => {
    const diff = endDate.getTime() - startDate.getTime();
    return (diff / 60000);
}

const decodeBase64 = (s) => {
    var e = {}, i, b = 0, c, x, l = 0, a, r = '', w = String.fromCharCode, L = s.length;
    var A = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    for (i = 0; i < 64; i++) { e[A.charAt(i)] = i; }
    for (x = 0; x < L; x++) {
        c = e[s.charAt(x)]; b = (b << 6) + c; l += 6;
        while (l >= 8) { ((a = (b >>> (l -= 8)) & 0xff) || (x < (L - 2))) && (r += w(a)); }
    }
    return r;
};

const stringFromHTML = (html) => {
    let div = document.createElement("DIV");
    div.innerHTML = html;

    const retorno = div.textContent || tmp.innerText || "";
    div = undefined;
    delete div;

    return '&nbsp;&nbsp; | &nbsp;&nbsp;' + retorno;
};

String.prototype.padLeft = function (character, number) {
    var a = this.split('');

    while (a.length < number) {
        a.unshift(character);
    }

    return a.join('');
}

String.prototype.replaceAll = function (search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

String.prototype.format = function () {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function (match, number) {
        return typeof args[number] != 'undefined'
          ? args[number]
          : match
        ;
    });
};

const stringToDate = (control) => {
    return new Date($('#' + control).val().replaceAll('-', '/'));
};

const getParamsFromUrl = (name) => {
    const url = location.href;
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regexS = "[\\?&]" + name + "=([^&#]*)";
    var regex = new RegExp(regexS);
    var results = regex.exec(url);
    return results == null ? null : results[1];
}

const createCookie = (name, value, days) => {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        var expires = "; expires=" + date.toGMTString();
    }
    else var expires = "";
    document.cookie = name + "=" + value + expires + "; path=/";
}

const readCookie = (name) => {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');

    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }

    return undefined;
}

const combo01 = (val) => {
    return parseInt(val) == 1 ? "Sim" : "N�o";
};

const comboFamilia = () => {
    let url = parent.id1 ? '' : '../'
    url += 'services/PRODUTO.asmx/comboFamilia';

    const data = {
        ID_EMPRESA: parent._sys1 ? parent.id1 : _idEmpresa,
        keep: parent.keep ? parent.keep : _id1
    };

    const success = function (response) {
        const data = eval(response.d);

        const combos = ['CB_FAMILIA_PRODUTO', 'CB_ID_FAMILIA'];

        combos.map(function (item) {
            $('#' + item).empty();

            if (item == 'CB_FAMILIA_PRODUTO')
                $('#' + item).append("<option value='0'>TODAS</option>");

            data.map(function (item1) {
                $('#' + item).append("<option value='" + item1.ID_FAMILIA + "'>" +
                    item1.DESCRICAO_FAMILIA + "</option>");
            });

            if (item == 'CB_FAMILIA_PRODUTO')
                $('#' + item).val(0);
        });
    }

    doranAjax(url, data, success);
};

const comboEmpresa = () => {
    const url = 'services/EMPRESA.asmx/comboEmpresa';
    const data = {
        keep: parent.keep
    };

    const success = function (response) {
        const data = eval(response.d);

        $('#TXT_ID_EMPRESA').empty();

        data.map(function (item) {
            $('#TXT_ID_EMPRESA').append("<option value='" + item.ID_EMPRESA + "'>" +
                item.NOME_FANTASIA + "</option>");
        });
    }

    doranAjax(url, data, success);
};

const comboProduto = () => {
    const url = 'services/PRODUTO.asmx/comboProduto';
    const data = {
        ID_EMPRESA: parent._sys1,
        keep: parent.keep
    };

    const success = function (response) {
        const data = eval(response.d);

        $('#CB_ID_PRODUTO').empty();

        data.map(function (item, i) {
            $('#CB_ID_PRODUTO').append("<option value='" + item.ID_PRODUTO + "'>" +
                item.DESCRICAO_PRODUTO + "</option>");

            if (i == 0) {
                $('#CB_ID_PRODUTO').val(item.ID_PRODUTO);
                $('#TXT_PRECO_COMANDA').val(item.PRECO_VENDA);
            }
        });
    }

    doranAjax(url, data, success);
};

const comboFornecedor = () => {
    const url = 'services/FORNECEDOR.asmx/comboFornecedor';
    const data = {
        ID_EMPRESA: parent._sys1,
        keep: parent.keep
    };

    const success = function (response) {
        const data = eval(response.d);

        $('#CB_ID_FORNECEDOR').empty();

        data.map(function (item, i) {
            $('#CB_ID_FORNECEDOR').append("<option value='" + item.ID_FORNECEDOR + "'>" +
                item.NOME_FANTASIA + "</option>");

            if (i == 0) {
                $('#CB_ID_FORNECEDOR').val(item.ID_FORNECEDOR);
            }
        });
    }

    doranAjax(url, data, success);
};

const applyMask = (fields, masks) => {
    fields.map(function (item, i) {
        $('#' + item).focusout(function () { doranMask(item, masks[i]); })
    });
};

const doranMask = (field, mask) => {
    let signs = [];
    let numbers = onlyNumbersFromString1($('#' + field).val()) + '';

    for (let i = 0; i < mask.length; i++) {
        if (mask.substring(i, (i + 1)) != '9')
            signs.push(i);
    }

    let starts = 0;

    signs.map(function (item, i) {

        const signal = mask.substring(signs[i], (signs[i] + 1));

        numbers = numbers.substring(starts, signs[i]) +
            signal + numbers.substr(signs[i]);
    });

    $('#' + field).val(numbers);
};

const aplyTouchSpin = (controls) => {
    controls.map(function (item) {
        $("input[name='" + item + "']").TouchSpin({
            min: 0,
            prefix: '',
            initval: 0,
            buttondown_class: "btn btn-warning",
            buttonup_class: "btn btn-success"
        });

        $('#' + item).attr('width', '120px');
    });
}

const separaNumeroEndereco = (endereco, ctrl) => {

    const end1 = endereco.lastIndexOf(' ');
    const end2 = endereco.lastIndexOf(',');

    if (end1 > -1 || end2 > -1) {
        let strNum = end1 > -1 ? parseInt(endereco.substring(end1)) > 0 ?
            parseInt(endereco.substring(end1)) : -1 : -1;

        if (strNum == -1)
            strNum = end2 > -1 ? parseInt(endereco.substring(end2)) > 0 ?
                parseInt(endereco.substring(end2)) : -1 : -1;

        if (parseInt(strNum) > -1)
            $('#' + ctrl).val(strNum + '');
    }
};

const currencyFormatted = (value) => {
    return 'R$ ' + parseFloat(value).formatMoney(2, ',', '.');
}

const preencheAnoValidade = () => {
    let options = $('#CB_ANO_VALIDADE');
    let options1 = $('#CB_MES_VALIDADE');

    let year = parseInt(new Date().getFullYear());
    let month = 1;

    options.empty();
    options1.empty();

    let selected = '';

    for (var i = 0; i < 12; i++) {
        selected = i == 0 ? 'selected' : '';

        options.append("<option value='" + year + "' " + selected + ">" +
            year + "</option>");

        options1.append("<option value='" + (month + '').padLeft('0', 2) + "' " + selected + ">" +
            (month + '').padLeft('0', 2) + "</option>");

        year++;
        month++;
    }
};

Number.prototype.formatMoney = function (c, d, t) {
    var n = this,
        c = isNaN(c = Math.abs(c)) ? 2 : c,
        d = d == undefined ? "." : d,
        t = t == undefined ? "," : t,
        s = n < 0 ? "-" : "",
        i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "",
        j = (j = i.length) > 3 ? j % 3 : 0;
    return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
};

String.prototype.startsWith = function (str) {
    return (this.indexOf(str, 0) == 0);
}

const carregaBandeiras = () => {

    const formaPagto = $('#CB_FORMA_PAGTO').val();

    const bandeira = $('#CB_BANDEIRA');
    bandeira.empty();

    const ctrls = ['CB_BANDEIRA', 'TXT_NOME_CARTAO', 'TXT_NUMERO_CARTAO',
        'TXT_COD_SEG', 'CB_MES_VALIDADE', 'CB_ANO_VALIDADE'];

    enableCtrl(ctrls, true);

    if (formaPagto == "Debito") {
        bandeira.append("<option value='Visa'>VISA</option>");
        bandeira.append("<option value='Maestro'>MAESTRO</option>");
    }

    else if (formaPagto == "Credito") {
        bandeira.append("<option value='Visa'>VISA</option>");
        bandeira.append("<option value='Master' selected>MASTERCARD</option>");
        bandeira.append("<option value='Amex'>AMEX</option>");
        bandeira.append("<option value='Elo'>ELO</option>");
        bandeira.append("<option value='Diners'>DINERS</option>");
        bandeira.append("<option value='Discover'>DISCOVER</option>");
        bandeira.append("<option value='JCB'>JCB</option>");
        bandeira.append("<option value='Aura'>AURA</option>");
        bandeira.append("<option value='Hipercard'>HIPERCARD</option>");
    }

    else if (formaPagto == "Dinheiro") {
        enableCtrl(ctrls, false);
    }
};

const enableCtrl = (controls, ed) => {
    controls.map(function (item) {
        if (ed) {
            $('#' + item).removeAttr('disabled');
        }
        else if (!ed) {
            $('#' + item).attr('disabled', 'disabled');
        }
    });
};

const distinct = (value, index, self) => { 
    return self.indexOf(value) === index;
};