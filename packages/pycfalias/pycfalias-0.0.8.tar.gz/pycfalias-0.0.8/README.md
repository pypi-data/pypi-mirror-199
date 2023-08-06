# pycfalias
Easy Cloudflare email alias management

### Installation

1. Install via python pip
   ```
   pip install pycfalias
   ```
2. Configure either via configuration file or environment variables
   ```
   export CF_FORWARD_EMAIL=$your_forward_email
   export CF_TOKEN=$your_cloudflare_token
   export CF_ZONE_ID=$your_cloudflare_zone_id
   ``` 
   OR

   Create a file in your home directory called ```.pycfalias.toml``` (note the dot)
   ```
   "CF_FORWARD_EMAIL" = "$your_forward_email"
   "CF_TOKEN" = "$your_cloudflare_token"
   "CF_ZONE_ID" = "$your_cloudflare_zone_id"
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

List email aliases
```
pycfalias -l [--list]
```

Create an email alias
```
pycfalias -c [--create]
```

Remove existing email alias
```
pycfalias -r [--remove]
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Inspiration - [cf-alias](https://github.com/dustinblackman/cf-alias)


