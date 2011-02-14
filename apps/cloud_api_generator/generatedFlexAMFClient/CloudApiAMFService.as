package com.aserver.flex.lib.CloudApi
{
    import flash.events.NetStatusEvent;
    import flash.events.SecurityErrorEvent;
    import flash.net.NetConnection;
    import flash.net.ObjectEncoding;
    import flash.net.Responder;

    import mx.controls.Alert;

    import org.as3yaml.YAML;
    
    public class CloudApiAMFService
    {
        private var CMC_NO_CLOUDAPI_CONNECTION:String = "Cloud Management Center was unable to connect to the server.\nThis could be due to the loss of network connection, a recent password change for the current user or the server was not responding. If the problem persists, please contact your IT support provider.";
        
        public static var sdkAddress:String = null;
        public static var login:String=null;
        public static var passwd:String=null;
        private var gateway:NetConnection = new NetConnection();
        public function CloudApiAMFService()
        {
            gateway.addEventListener(NetStatusEvent.NET_STATUS, netStatusHandler);
            gateway.addEventListener(SecurityErrorEvent.SECURITY_ERROR, securityErrorHandler);
        }
        public function connect():void{
            if (gateway.connected == true)
                return

            //var httpUrl:String = "http://" + sdkAddress + ":8899";//"/appserver/amf/";                        
            var httpUrl:String = "http://" + sdkAddress + "/appserver/amf/";
            gateway.connect( httpUrl );

            // Authentication
            gateway.addHeader( "Credentials", false, {userid: login, password: passwd} );
        }
        public function reconnect():void{
            if (gateway.connected == false)
                gateway = new NetConnection();

            connect();
        }
        public function disconnect():void{
            if (gateway.connected == true)
                gateway.close();
        }
        public function callMethod(service:String, methodName:String, onResult:Function, onError:Function, ... arguments):void{
            connect();

            var serviceCall:String = service+"."+methodName;

            var responder:Responder = new Responder( onResult, onError );

            if (arguments != null && arguments.length >0){
                var args:Array = new Array;
                args.push(serviceCall);
                args.push(responder);

                for each (var arg:Object in arguments){
                  args.push(arg);
                }

                var callFunction:Function = gateway.call;
                callFunction.apply(gateway, args);
              }else
                   gateway.call( serviceCall, responder);
        }

        private function netStatusHandler(event:NetStatusEvent):void {
            if (event.info.code == "NetConnection.Call.Failed")
                Alert.show(CMC_NO_CLOUDAPI_CONNECTION);
        }

        private function securityErrorHandler(event:SecurityErrorEvent):void {
        }

        public static function GetResult(result:*):Object
        {
            return result.result;
        }

        public static function GetYamlResult(result:*):Object
        {
            return YAML.decode(GetResult(result).toString());
        }
    }
}
