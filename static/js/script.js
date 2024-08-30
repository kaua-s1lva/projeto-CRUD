$(document).ready(function() {
    // Carregar os itens ao iniciar a página
    loadItems();

    // Botão para abrir o modal de adicionar item
    $('#addItemBtn').on('click', function() {
        $('#itemModalLabel').text('Adicionar Item');
        $('#itemForm')[0].reset();
        $('#itemId').val('');
        $('#itemForm').removeClass('was-validated'); // Limpa as mensagens de erro
        $('#itemModal').modal('show');
    });

    // Salvar item (novo ou editado)
    $('#saveItemBtn').on('click', function() {
        if (validateForm()) {
            const id = $('#itemId').val();
            const item = {
                nome: $('#nome').val(),
                valor: parseFloat($('#valor').val()),
                quantidade: parseInt($('#quantidade').val(), 10),
                item_especial: $('#item_especial').val() === 'true',
                ingredientes: $('#ingredientes').val().split(',').map(i => i.trim())
            };

            if (id) {
                // Editar item existente
                $.ajax({
                    url: '/items/' + id,
                    type: 'PUT',
                    contentType: 'application/json',
                    data: JSON.stringify(item),
                    success: function() {
                        $('#itemModal').modal('hide');
                        loadItems();
                    }
                });
            } else {
                // Adicionar novo item
                $.ajax({
                    url: '/items',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(item),
                    success: function() {
                        $('#itemModal').modal('hide');
                        loadItems();
                    }
                });
            }
        }
    });

    function validateForm() {
        let isValid = true;
        
        // Remove validação anterior
        $('.form-control').removeClass('is-invalid');
        
        // Verifica se o nome está vazio
        if (!$('#nome').val().trim()) {
            $('#nome').addClass('is-invalid');
            isValid = false;
        }
        
        // Verifica se o valor é um número válido
        if (isNaN(parseFloat($('#valor').val()))) {
            $('#valor').addClass('is-invalid');
            isValid = false;
        }
        
        // Verifica se a quantidade é um número válido
        if (isNaN(parseInt($('#quantidade').val(), 10))) {
            $('#quantidade').addClass('is-invalid');
            isValid = false;
        }
        
        // Verifica se o item especial foi selecionado
        if ($('#item_especial').val() === '') {
            $('#item_especial').addClass('is-invalid');
            isValid = false;
        }
        
        // Verifica se ingredientes foram fornecidos
        if (!$('#ingredientes').val().trim()) {
            $('#ingredientes').addClass('is-invalid');
            isValid = false;
        }
        
        return isValid;
    }

    // Editar item
    $(document).on('click', '.editItemBtn', function() {
        const id = $(this).data('id');
        $.getJSON('/items/' + id, function(item) {
            $('#itemId').val(item.id);
            $('#nome').val(item.nome);
            $('#valor').val(item.valor);
            $('#quantidade').val(item.quantidade);
            $('#item_especial').val(item.item_especial ? 'true' : 'false');
            $('#ingredientes').val(item.ingredientes.join(', '));
            $('#itemModalLabel').text('Editar Item');
            $('#itemModal').modal('show');
        });
    });

    // Excluir item
    $(document).on('click', '.deleteItemBtn', function() {
        const id = $(this).data('id');
        if (confirm('Tem certeza que deseja excluir este item?')) {
            $.ajax({
                url: '/items/' + id,
                type: 'DELETE',
                success: function() {
                    loadItems();
                }
            });
        }
    });

    function loadItems() {
        $.getJSON('/items', function(data) {
            var items = data.items;
            var itemsTableBody = $('#itemsTableBody');
            itemsTableBody.empty();

            items.forEach(function(item) {
                if (!item.excluido) {
                    var row = `<tr>
                        <td>${item.nome}</td>
                        <td>${item.valor.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                        <td>${item.quantidade}</td>
                        <td>${item.item_especial ? 'Sim' : 'Não'}</td>
                        <td>${new Date(item.data_emissao).toLocaleString()}</td>
                        <td>
                            <button class="btn btn-warning btn-sm editItemBtn" data-id="${item.id}">Editar</button>
                            <button class="btn btn-danger btn-sm deleteItemBtn" data-id="${item.id}">Excluir</button>
                        </td>
                    </tr>`;
                    itemsTableBody.append(row);
                }
            });
        });
    }
});
