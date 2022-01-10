      paypal.Buttons({

        // Sets up the transaction when a payment button is clicked
        createOrder: function(data, actions) {
          return actions.order.create({
            purchase_units: [{
              amount: {
                value: '0.44' // Can reference variables or functions. Example: `value: document.getElementById('...').value`
              }
            }]
          });
        },

        // Finalize the transaction after payer approval
        onApprove: function(data, actions) {
          return actions.order.capture().then(function(orderData) {
            var transaction = orderData.purchase_units[0].payments.captures[0];
                var document = document.getElementById('paypal-button-container');

              //var receipt_details = `
                //<div>
                  //  <h1>PAYMENT SUCCESSFUL</h1>
                    //<p> Transaction number:${transaction.id}</p>
                    //<p>Time:${transaction.update_time}</p>
                    //<>p>Total:${transaction.value}</p>
                    //<p> Thank you for purchasing with us! We hope to see you again</p>
                //</div>`
                //transaction.innerHTML = receipt_details;

              location.replace('success_payment.html')


            // Successful capture! For dev/demo purposes:
                console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));
                var transaction = orderData.purchase_units[0].payments.captures[0];
                alert('Transaction'+ transaction.id + ': ' + transaction.update_time + transaction.amount.value+ '\n\nSee console for all available details');

            //When ready to go live, remove the alert and show a success message within this page. For example:
            // var element = document.getElementById('paypal-button-container');
            // element.innerHTML = '';
            // element.innerHTML = '<h3>Thank you for your payment!</h3>';
            // Or go to another URL:  actions.redirect('thank_you.html');
          });
        }


      }).render('#paypal-button-container');

