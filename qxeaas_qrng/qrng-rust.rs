use dotenv
use reqwest
use serde::Deserialize;

#[derive(Debug, Deserialize)]
struct Response {
    pub random_number: String,
    pub message: String
}

fn main() -> Result<(), reqwest::Error> {
    dotenv().ok(); // Load environment variables from .env file

    let access_token = std::env::var("ACCESS_TOKEN")?;
    let size = // Replace with the required size for your application

    let url = format!("https://api-qxeaas.quantumemotion.com/entropy");

    let client = reqwest::Client::new();
    let mut headers = reqwest::header::HeaderMap::new();
    headers.insert(
        reqwest::header::AUTHORIZATION,
        format!("Bearer {}", access_token).parse()?,
    );

    let params = [("size", size.to_string())];

    let response = client
        .get(url)
        .headers(headers)
        .query(&params)
        .send()?
        .json::<Response>()?;

    println!("response => {:?}", response);

    Ok(())
}

