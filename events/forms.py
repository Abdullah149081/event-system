from django import forms
from events.models import Event, Category


class TailwindMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxSelectMultiple):

                existing_classes = widget.attrs.get("class", "")
                widget.attrs["class"] = (
                    f"{existing_classes} space-y-2 p-4 bg-gray-50 border border-gray-200 rounded-lg"
                ).strip()

                widget.attrs.update(
                    {"style": "display: flex; flex-direction: column; gap: 8px;"}
                )
            elif isinstance(widget, forms.Select):
                existing_classes = widget.attrs.get("class", "")
                widget.attrs["class"] = (
                    f"{existing_classes} appearance-none w-full bg-white/80 text-gray-900 font-medium px-4 py-3 pr-10 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-yellow-300 cursor-pointer shadow-sm transition-transform duration-200 group-focus-within:scale-105"
                ).strip()
            elif isinstance(widget, (forms.DateInput, forms.TimeInput)):
                existing_classes = widget.attrs.get("class", "")
                widget.attrs["class"] = (
                    f"{existing_classes} w-full shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-yellow-300 focus:border-yellow-300"
                ).strip()
            elif isinstance(widget, forms.Textarea):
                existing_classes = widget.attrs.get("class", "")
                widget.attrs["class"] = (
                    f"{existing_classes} w-full shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-yellow-300 focus:border-yellow-300 resize-vertical min-h-[80px]"
                ).strip()
            else:
                existing_classes = widget.attrs.get("class", "")
                widget.attrs["class"] = (
                    f"{existing_classes} w-full shadow appearance-none border rounded py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-yellow-300 focus:border-yellow-300"
                ).strip()


class EventForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "date",
            "time",
            "location",
            "category",
            "image",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
            "image": forms.FileInput(
                attrs={
                    "accept": "image/*",
                    "class": "block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100",
                }
            ),
        }
        help_texts = {
            "image": "Upload an image for your event. Images will be automatically optimized to WebP format for better performance.",
        }

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:

            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 10MB )")

            try:
                from PIL import Image as PILImage

                PILImage.open(image)
                image.seek(0)
            except Exception:
                raise forms.ValidationError("Invalid image file")

        return image


class CategoryForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
