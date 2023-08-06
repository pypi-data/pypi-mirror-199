from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.forms import (
    CharField,
    FloatField,
)

from dcim.models import Platform
from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)
from netbox_storage.models import Drive, StorageConfigurationDrive, TemplateConfigurationDrive, LinuxDevice
from utilities.forms import (
    CSVModelChoiceField,
    DynamicModelChoiceField,
)
from virtualization.models import Cluster, ClusterType, VirtualMachine


class DriveForm(NetBoxModelForm):
    """Form for creating a new Drive object."""
    # ct = ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the drive e.g. 25",
        validators=[MinValueValidator(1)],
    )
    cluster_type = DynamicModelChoiceField(
        queryset=ClusterType.objects.all(),
        help_text="The Cluster Type of the drive",
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        query_params={
            'type_id': '$cluster_type'  # ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
        },
        help_text="The Storage Cluster of the drive",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Hard Drive 1 on SSD Cluster",
    )

    class Meta:
        model = Drive

        fields = (
            "size",
            "cluster",
            "description",
        )


class DriveCreateForm(NetBoxModelForm):
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the drive e.g. 25",
        validators=[MinValueValidator(1)],
    )
    cluster_type = DynamicModelChoiceField(
        queryset=ClusterType.objects.all(),
        help_text="The Cluster Type of the drive",
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        query_params={
            'type_id': '$cluster_type'  # ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
        },
        help_text="The Storage Cluster of the drive",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Hard Drive 1 on SSD Cluster",
    )

    virtual_machine = DynamicModelChoiceField(
        required=False,
        label="Virtual Machine",
        queryset=VirtualMachine.objects.all(),
        help_text="Mapping between drive and virtual machine  e.g. vm-testinstall-01",
    )
    platform = DynamicModelChoiceField(
        required=False,
        label="Platform",
        queryset=Platform.objects.all(),
        help_text="Mapping between drive and platform  e.g. Rocky Linux 9",
    )

    class Meta:
        model = Drive

        fields = (
            "size",
            "cluster",
            "description",
        )

    def save(self, *args, **kwargs):
        if self.cleaned_data['virtual_machine']:
            number_of_hard_drives = StorageConfigurationDrive.objects.filter(virtual_machine=self.cleaned_data['virtual_machine']).count() or 0
            self.instance.identifier = f'Hard Drive {number_of_hard_drives + 1}'
            drive = super().save(*args, **kwargs)
            StorageConfigurationDrive.objects.create(virtual_machine=self.cleaned_data['virtual_machine'], drive=drive)
        else:
            number_of_hard_drives = TemplateConfigurationDrive.objects.filter(platform=self.cleaned_data['platform']).count() or 0
            self.instance.identifier = f'Hard Drive {number_of_hard_drives + 1}'
            drive = super().save(*args, **kwargs)
            if 'windows' not in str(self.cleaned_data['platform']).lower():
                drive_type_pk = ContentType.objects.get(app_label='netbox_storage', model='drive').pk
                LinuxDevice.objects.create(device=drive.device_name(),
                                           type='Disk',
                                           size=self.cleaned_data['size'],
                                           object_id=drive.pk,
                                           content_type_id=drive_type_pk)
            TemplateConfigurationDrive.objects.create(platform=self.cleaned_data['platform'], drive=drive)
        return drive


class DriveEditForm(NetBoxModelForm):
    size = FloatField(
        label="Size (GB)",
        help_text="The size of the drive e.g. 25",
        validators=[MinValueValidator(0.1)],
    )
    cluster_type = DynamicModelChoiceField(
        required=False,
        queryset=ClusterType.objects.all(),
        help_text="The Cluster Type of the drive",
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        query_params={
            'type_id': '$cluster_type'  # ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
        },
        help_text="The Storage Cluster of the drive",
    )
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. Hard Drive 1 on SSD Cluster",
    )

    fieldsets = (
        (
            "Drive Configuration Items",
            (
                "cluster_type",
                "cluster",
                "size",
                "description"
            ),
        ),
    )

    class Meta:
        model = Drive

        fields = (
            "size",
            "cluster",
            "description",
        )

    def save(self, *args, **kwargs):
        drive = super().save(*args, **kwargs)
        drive_type_pk = ContentType.objects.get(app_label='netbox_storage', model='drive').pk
        linux_device_drive = LinuxDevice.objects.get(object_id=drive.pk,content_type_id=drive_type_pk)
        linux_device_drive.size = self.cleaned_data['size']
        linux_device_drive.save()
        return drive


class DriveFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering Drive instances."""

    model = Drive

    size = FloatField(
        required=False,
        label="Size (GB)",
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(
            # type__pk=ClusterType.objects.filter(name="Storage").values_list('id', flat=True)[0]
        ),
        required=False,
    )


class DriveImportForm(NetBoxModelImportForm):
    cluster = CSVModelChoiceField(
        queryset=Cluster.objects.all(),
        to_field_name='name',
        required=False,
        help_text='Assigned cluster'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Drive

        fields = (
            "size",
            "cluster",
            "description",
        )


class DriveBulkEditForm(NetBoxModelBulkEditForm):
    model = Drive

    size = FloatField(
        required=False,
        label="Size (GB)",
    )
    cluster = DynamicModelChoiceField(
        queryset=Cluster.objects.all(),
        required=False,
        query_params={
            'site_id': '$site'
        }
    )
    description = CharField(max_length=255, required=False)

    fieldsets = (
        (
            None,
            ("size", "cluster", "description"),
        ),
    )
    nullable_fields = ["description"]
