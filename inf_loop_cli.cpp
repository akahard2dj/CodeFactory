void CommandLineInterface::command_line_interface_loop()
{	
    bool connectedAardvark = false;
    bool connectedWFS = false;

    char buf[1024];
    
    cout << ">>> ";
    while (fgets(buf, sizeof(buf), stdin)) {
        size_t len = strlen(buf);

        if (len != 1) {
            char *pBuf, *context;
            pBuf = strtok_s(buf, "\n", &context);
            string inputStr(pBuf);
            vector<string> inputArguments;
            inputArguments = get_token(inputStr);

            if (inputArguments.at(0).compare("test") == 0) {
                
            }
          
            if (inputArguments.at(0).compare("quit") == 0) {
                break;
            }           
        }	
        cout << ">>> ";
    }
}
