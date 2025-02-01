# Django CLI

This CLI tool currently generates a standardized Python-based web application with styling. A project can be generated as a "vue-vite" Django-only application or as a monolithic application with Django + Djangorestframework + Vue.js 3 single-page-app configuration.

The project includes:
- Django 4
- Bootstrap 5.2 + Bootstrap Icons
- Docker Compose setup with Postgres database
- Deployment ready Docker build with Uvicorn web server
- flake8 linting rules

For the Vue.js template, in addition to the above:
- Vue.js 3
- Vue Router
- Pinia for state management
- eslint rules
- Google Analytics support in Vue.js
- Vite-optimized build for production, with minified and compressed asset handling
- Multi-stage Docker build

## Notes

- Github Actions are included for automated linting and vulnerability scanning. Additional examples can be provided for Docker build and push actions to either Dockerhub or Github Container Registry (GHCR).

- There may be more dependencies than needed for your use-case. Remove them from requirements.txt and package.json as necessary. For example, you may not need a centralized store for state management in Vue and Pinia can be removed.

# Steps to Use

1. Run `init.sh`, which will install or update the CLI dependencies in a virtual environment.
2. [Activate the virtual environment.](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments)
3. Run the CLI tool with the desired arguments.

```bash
# Mac OS/Linux; steps may differ slightly for Windows
./init.sh
source ./venv/bin/activate
python3 -u scaffold.py PROJECT_NAME [PATH_ON_YOUR_MACHINE_WHERE_YOU_WANT_THE_PROJECT]
```

If you want to see what additional arguments are supported, run `python3 -u scaffold.py --help`.

# Pre-production Checklist

- Create unique secret keys for Django with sufficient entropy. If you open up a Django REPL, you can do the following to generate a key which can be copied + pasted to your environment:
    ```python
    from django.core.management.utils import get_random_secret_key
    get_random_secret_key()
    ```
- Set `WHITENOISE_MAX_AGE` to an appropriate duration (in seconds) to optimize browser caching of static assets and reduce server load. For example, setting this to 86400 will make sure that a user's browser will utilize cache for 24 hours before fetching again.
- Make sure `FORWARDED_ALLOW_IPS=*` in your environment variables so that proxy headers are properly respected in server logs. In a deployment to OpenShift or in a hosted MiServer environment behind a reverse proxy (such as Apache), Uvicorn will need to instead use forwarded IP headers instead of the remote address.
- Create your Shibboleth request and configure OIDC according to mozilla-django-oidc instructions
- (Optional) Add `WORKERS_PER_CORE=2` to your environment variables. The optimized gunicorn.conf.py config file will automatically set the Gunicorn worker count based on how many CPUs are available, but [Gunicorn has suggested in their documentation](https://docs.gunicorn.org/en/stable/design.html#how-many-workers) that `(2 x $num_cores) + 1` is an appropriate formula to begin with.

# Developer Notes

## Routine upgrade process

It is a good practice to update dependencies regularly to address bugs and vulnerabilities. The following steps can be performed for a project that is created with this template:

1. Upgrade your Python libraries.

    Note that this process will update according to the strategy defined in requirements.txt. In this template, we are using the `~=` terminology which means that with each new Docker build, the latest compatible version will be installed. There is no guarantee that this process will not introduce a breaking change, so test as always and bump major versions manually in requirements.txt if you are ready to move up further.

    ```bash
    docker-compose build --no-cache --pull
    docker-compose up [-d]
    docker-compose exec api pip freeze > src/requirements.prod.txt

    # optional diff the package changes
    git diff
    git add src/requirements.prod.txt
    git commit -m "Upgrade Python libraries to latest compatible"
    ```

2. <strong>(Django + Vue.js template only)</strong> Upgrade your npm packages.

    Manually bump up any major versions in package.json first before running `npm upgrade` if necessary, or it will otherwise upgrade to the latest patch version via the `^` descriptor.

    ```bash
    # assumes frontend container is running under Docker Compose

    # optional, audit current packages
    docker-compose exec frontend npm audit

    # also optional, list outdated including those without known vulnerabilities
    docker-compose exec frontend npm outdated

    # upgrade packages
    docker-compose exec frontend npm upgrade
    git add src/assets/package-lock.json
    git commit -m "Upgrade npm packages to latest compatible"
    ```

3. (Optional) Upgrade Python version.

    The Python version that you use for your application is not critical so long as it is maintained still for bugs/vulnerabilities.

    If you want to change the Python version anyway, you can simply change the base layer in your Dockerfile and Dockerfile.prod and rebuild, making sure to test appropriately. You can then also update the versions as necessary in any Github Actions described in `.github/workflows` to stay at parity with your project.

4. <strong>(Django + Vue.js template only)</strong> Upgrade Node version.

    It is recommended that you keep your node version on the [LTS release](https://nodejs.org/en/). Update the base layer in both Dockerfiles and in the relevant `.github/workflows`, similar to step 3 regarding Python.

## Testing a production build

In a production setting, Python library versions are locked explicitly to certain versions to prevent any unintended side-effects between builds. If you want to simulate this process locally for your generated project, it is possible using `docker-compose.prod.yml`. The commands below can be used or you can execute `scripts/test_prod.sh` for the same effect.

```bash
docker-compose down
docker-compose -f docker-compose.prod.yml build --no-cache --pull
docker-compose -f docker-compose.prod.yml up
```

When you are finished and want to switch back to the development Compose setup, you can perform the same steps as above minus the `-f docker-compose.prod.yml` argument.

# Future

- Allow specifying database type for generating standardized setups with MySQL, OracleDB, etc.
- Consider Poetry over pip for better dependency management
