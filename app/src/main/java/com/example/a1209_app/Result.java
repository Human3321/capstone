package com.example.a1209_app;

public class Result {
    public static String result;

    private static final Result instance = new Result();

    private Result() {};
    public static Result Getinstance()
    {
        return instance;
    }


    public Result (String result){
        this.result = result;
    }

    public void setResult(String result) {
        this.result = result;
    }

    public String getResult() {
        return result;
    }
}
