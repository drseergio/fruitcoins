Ext.regController('Receipt', {
  index: function() {
    if  (navigator) {
      navigator.camera.getPicture(onSuccess, onFail, {
        quality: 50,
        sourceType: Camera.PictureSourceType.CAMERA,
        targetHeight: 1200,
        targetWidth: 1200 });

      function onSuccess(imageData) {
        Ext.Msg.confirm("Receipt upload",
          "Upload this receipt?",
          function(btn) {
            if (btn == "yes") {
              navigator.geolocation.getCurrentPosition(
                function(position) {
                  Ext.Ajax.request({
                    params: {
                      image: imageData,
                      latitude: position.coords.latitude,
                      longitude: position.coords.longitude
                    },
                    url: fruitcoinsUrl + 'api/receipt/upload',
                    method: 'POST',
                    success: function(response) {
                      var data = Ext.util.JSON.decode(response.responseText);
                      if (data.success) {
                        Ext.Msg.alert('Done!', 'Successfully uploaded receipt');
                      } else {
                        Ext.Msg.alert('Failed', data.errors[0].msg);
                      }
                    },
                    failure: function() {
                      Ext.Msg.alert('Failed', 'Failed to upload receipt');
                    }
                  });
                }, 
                function() {
                  Ext.Ajax.request({
                    params: {
                      image: imageData,
                    },
                    url: fruitcoinsUrl + 'api/receipt/upload',
                    method: 'POST',
                    success: function() {
                      var data = Ext.util.JSON.decode(response.responseText);
                      if (data.success) {
                        Ext.Msg.alert('Done!', 'Successfully uploaded receipt');
                      } else {
                        Ext.Msg.alert('Failed', data.errors[0].msg);
                      }
                    },
                    failure: function() {
                      Ext.Msg.alert('Failed', 'Failed to upload receipt');
                    }
                  });
                });
            }
        });
      }

      function onFail(message) {
      }
    } else {
      if (!this.receiptView) {
        this.receiptView = this.render({
          xtype: 'receipts',
        });
      }
 
      this.application.viewport.setActiveItem(this.receiptView);
      }
  },
});