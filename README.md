# AWS Lambda Septime

See blog at: https://medium.com/@stephane.maarek/how-i-used-aws-lambda-to-hack-my-way-into-eating-at-septime-41c7dcd8f861

# Running

Install serverless 
```bash
npm install -g serverless
```

Get an [API key](https://docs.pushbullet.com/) for Pushbullet and upload your Pushbullet API key in SSM Parameter Store as a Secure String at:
```bash
/septime/pushbullet_api_key
```

Configure your AWS credentials
```bash
aws configure --profile name-your-profile
```

Edit [serverless.yml](serverless.yml) with your AWS profile `name-your-profile` instead of the existing one

Deploy the function
```bash
sls deploy -v
```

**Eat good food**

# Links / Resources

- [Serverless website](https://serverless.com)
- [Serverless python plugin](https://github.com/UnitedIncome/serverless-python-requirements)
- [Udemy AWS Lambda & Serverless Framework Course](https://www.udemy.com/aws-lambda-serverless/?couponCode=GITHUB10)
- [Udemy AWS Certified Developer Course](https://www.udemy.com/aws-certified-developer-associate-dva-c01/?couponCode=GITHUB10) 
