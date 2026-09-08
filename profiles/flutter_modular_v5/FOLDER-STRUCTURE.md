# Folder Structure: Flutter Modular v5

Follow the legacy project structure: app routing modules in `lib/routes/`, service/repository infrastructure in `lib/services/`, business state in `lib/cubit/`, and screens/components in `lib/ui/`. Each route-domain module remains near `lib/routes/`; do not introduce v6 feature `config/` modules or v7 `createModule` files.
